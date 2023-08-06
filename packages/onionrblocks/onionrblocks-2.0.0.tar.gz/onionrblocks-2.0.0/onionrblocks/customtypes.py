from collections import namedtuple
from typing import NewType


AnonymousVDFBlockResult = namedtuple(
    'AnonymousVDFBlockResult', ['dec_checksum', 'raw_bytes'])

HexChecksum = NewType("HexChecksum", str)
DecChecksum = NewType("DecChecksum", int)
DecChecksumStr = NewType("DecChecksumStr", str)
RawEd25519PrivateKey = NewType("RawEd25519PrivateKey", bytes)
RawEd25519PublicKey = NewType("RawEd25519PublicKey", bytes)
