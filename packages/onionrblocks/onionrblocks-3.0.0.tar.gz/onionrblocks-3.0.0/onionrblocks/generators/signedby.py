from hashlib import sha3_256
from typing import Union

from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError
from kasten import generator, Kasten
from kasten.exceptions import InvalidID
from kasten.types import KastenPacked, KastenChecksum

from onionrblocks.customtypes import RawEd25519PrivateKey, RawEd25519PublicKey
from onionrblocks.universalrules import check_block_sanity

class Signed(generator.KastenBaseGenerator):

    @classmethod
    def generate(
            cls,
            packed_bytes: KastenPacked,
            signingKey: Union[SigningKey, RawEd25519PrivateKey]
            ) -> Kasten:
        """Sign a digest of packed bytes, return a Kasten instance of it."""
        # Use libsodium/pynacl (ed25519)
        hashed = sha3_256(packed_bytes).digest()
        try:
            signed = signingKey.sign(hashed)
        except AttributeError:
            signingKey = SigningKey(signingKey)
            signed = signingKey.sign(hashed)
        # The KastenChecksum will be 64 bytes message then 32 bytes of the hash
        # This can be fed right back into VerifyKey without splitting up
        return Kasten(signed, packed_bytes, None,
                      auto_check_generator=False)


    @staticmethod
    def validate_id(
            hash: KastenChecksum,
            packed_bytes: KastenPacked,
            verify_key: Union[VerifyKey, RawEd25519PublicKey]) -> None:
        check_block_sanity(packed_bytes)
        # Hash is 64 bytes message then 32 bytes of the hash of the packed_bytes
        if len(hash) != 86:
            raise InvalidID("Block not have proper signature length")
        actual_hash = sha3_256(packed_bytes).digest()
        if not isinstance(verify_key, VerifyKey):
            verify_key = VerifyKey(verify_key)

        # Ensure that the digest is correct
        # Done in addition of the signature bc the sha3 can still ID blocks
        # and to prevent swapping sigs
        if actual_hash != hash[64:]:
            raise InvalidID("Invalid sha3_256 digest")
        # Ensure that the signature is correct
        try:
            verify_key.verify(hash)
        except BadSignatureError as e:
            raise InvalidID(repr(e))
