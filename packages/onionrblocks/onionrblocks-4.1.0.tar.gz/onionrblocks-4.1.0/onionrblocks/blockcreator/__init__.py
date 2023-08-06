"""
Copyright (C) <2020>  Kevin Froman

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from time import time

from kasten import Kasten
from kasten.generator.pack import pack

from ..generators import anonvdf


def create_anonvdf_block(
        block_data: bytes,
        block_type: bytes,
        ttl: int,
        **block_metadata) -> Kasten:
    try:
        block_data = block_data.encode('utf-8')
    except AttributeError:
        pass
    try:
        block_type = block_type.encode('utf-8')
    except AttributeError:
        pass
    ts = int(time())
    packed = pack(
        block_data, block_type,
        app_metadata=block_metadata, timestamp=ts)
    rounds_needed = anonvdf.AnonVDFGenerator.get_rounds_for_ttl_seconds(
        ttl, len(packed) + 10)
    block_metadata['rds'] = rounds_needed
    packed = pack(
        block_data,
        block_type, app_metadata=block_metadata, timestamp=ts)
    return anonvdf.AnonVDFGenerator.generate(
        packed, block_metadata['rds'])

