import time

from kasten import Kasten, generator
from kasten.types import KastenPacked, KastenChecksum
from kasten.exceptions import InvalidID

from mimcvdf import vdf_create, vdf_verify

from onionrblocks.universalrules import check_block_sanity
from onionrblocks.exceptions import BlockExpired


class NotEnoughRounds(Exception):
    pass


class AnonVDFGenerator(generator.KastenBaseGenerator):

    # 90000 rounds = 1 second (2.8ghz C) = 1 hour storage of 1 MB storage
    # jan 2021 disk price metric = 0.000017 USD per MB
    # mobile MB transfer US/Canada = 0.0125 USD
    # Max cost of block storage + American mobile data transfer = 0.0751 USD
    # Goal: approximately 2 seconds of computation for 1 hour of 1 MB storage

    byte_cost = 10
    second_cost = 4

    @classmethod
    def get_rounds_for_ttl_seconds(cls, seconds: int, size_bytes: int):
        return (seconds * cls.second_cost) + (size_bytes * cls.byte_cost)

    @classmethod
    def get_ttl_seconds_per_rounds(cls, rounds: int, size_bytes: int):
        return (rounds - (size_bytes * cls.byte_cost)) // cls.second_cost

    @classmethod
    def generate(
            cls, packed_bytes: KastenPacked, rounds: int = None) -> Kasten:
        if not rounds:
            try:
                rounds = int(Kasten(
                    None,
                    packed_bytes, None,
                    auto_check_generator=False).get_metadata()['rds'])
            except (KeyError, TypeError) as _:  # noqa
                raise ValueError(
                    "Rounds not specified either in block or as argument")
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
            packed_bytes: KastenPacked, rounds: int = None) -> None:

        check_block_sanity(packed_bytes)

        if not rounds:
            try:
                rounds = int(Kasten(
                    None,
                    packed_bytes, None,
                    auto_check_generator=False).get_metadata()['rds'])
            except (KeyError, TypeError) as _:  # noqa
                raise ValueError(
                    "Rounds not specified either in block or as argument")

        test_obj = Kasten(
            None, packed_bytes, None, auto_check_generator=False)
        allowed_age_seconds = AnonVDFGenerator.get_ttl_seconds_per_rounds(
            rounds, len(packed_bytes))
        if time.time() > test_obj.get_timestamp() + allowed_age_seconds:
            raise BlockExpired(
                f"Block rounds only valid through {allowed_age_seconds}")

        try:
            hash = int.from_bytes(hash, byteorder="big")
        except TypeError:
            pass
        if not vdf_verify(packed_bytes, hash, rounds):
            raise InvalidID

        return None