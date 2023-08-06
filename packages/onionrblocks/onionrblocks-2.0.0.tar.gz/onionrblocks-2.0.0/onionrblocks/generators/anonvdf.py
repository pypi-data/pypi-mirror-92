import time

from kasten import Kasten, generator
from kasten.types import KastenPacked, KastenChecksum
from kasten.exceptions import InvalidID

from mimcvdf import vdf_create, vdf_verify

from onionrblocks.universalrules import check_block_sanity

class AnonVDFGenerator(generator.KastenBaseGenerator):
    @classmethod
    def get_ttl_seconds_per_rounds(cls, rounds: int, size_bytes: int):
        # 90000 rounds = 1 second (2.8ghz C) = 1 hour storage of 1 MB storage
        # jan 2021 disk price metric = 0.000017 USD per MB
        # mobile MB transfer US/Canada = 0.0125 USD
        # Max cost of block storage + American mobile data transfer = 0.0751 USD

        base = 90000
        per_byte = 1000
        minimum = base + (per_byte * size_bytes)
        if rounds < minimum:
            raise ValueError(
                "Must be at least " + str(minimum) + " for " + str(size_bytes))

        return (rounds / minimum) * 60

    @classmethod
    def generate(
            cls, packed_bytes: KastenPacked, rounds: int = 90000) -> Kasten:
        check_block_sanity(packed_bytes)
        return Kasten(
            vdf_create(
                packed_bytes,
                rounds, dec=True
                ).to_bytes(
                    64, "big"), packed_bytes, cls, auto_check_generator=False)

    @staticmethod
    def validate_id(
            hash: KastenChecksum,
            packed_bytes: KastenPacked, rounds=90000) -> None:

        check_block_sanity(packed_bytes)

        try:
            hash = int.from_bytes(hash, byteorder="big")
        except TypeError:
            pass
        if not vdf_verify(packed_bytes, hash, rounds):
            raise InvalidID

        test_obj = Kasten(
            None, packed_bytes, None, auto_check_generator=False)
        allowed_age_seconds = AnonVDFGenerator.get_ttl_seconds_per_rounds(
            rounds, len(packed_bytes))
        if time.time() > test_obj.get_timestamp() + allowed_age_seconds:
            raise ValueError(
                f"Block rounds only valid through {allowed_age_seconds}")

        return None