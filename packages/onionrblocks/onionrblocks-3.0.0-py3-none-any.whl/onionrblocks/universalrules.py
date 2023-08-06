from kasten import Kasten

from time import time
from math import floor
from typing import Iterable

import binascii

MAX_FUTURE_SKEW_SECONDS = 60 * 2
TOTAL_MAX_SIZE = 6 * (10**6)


class BlockRulesException(Exception):
    pass


class BlockExpired(BlockRulesException):
    pass

class BlockFutureSkewedBeyondMax(BlockRulesException):
    pass

class BlockExistsError(BlockRulesException):
    pass

class BlockTooLarge(BlockRulesException):
    pass


def checksum_exists_in_list(checksum: bytes, arr: 'Iterable'):
    if checksum in arr:
        raise BlockExistsError(
            binascii.hexlify(
                checksum).decode("utf-8") + " Already exists in given set")


def check_block_sanity(raw_bytes):
    kasten: Kasten = Kasten(None, raw_bytes, None, auto_check_generator=False)

    # Ensure a block is not too large
    if len(kasten.get_packed()) > TOTAL_MAX_SIZE:
        raise BlockTooLarge()

    # Ensure block is not future-skewed or expired
    timestamp: int = floor(time())
    block_timestamp = kasten.get_timestamp()
    difference = timestamp - block_timestamp

    if difference < -MAX_FUTURE_SKEW_SECONDS:
        raise BlockFutureSkewedBeyondMax()

    try:
        if block_timestamp + kasten.get_metadata()['expire'] >= timestamp:
            raise BlockExpired()
    except (IndexError, TypeError, KeyError):
        pass


