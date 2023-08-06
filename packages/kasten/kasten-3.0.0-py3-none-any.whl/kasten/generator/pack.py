

"""Compile Kasten elements into a packed (msgpack) sequence.

KastenPacked sequences are prepared sequences used by Kasten instances and
their generators to apply rules and validation to Kasten.

Note that encryption and signing are not handled by anything in kasten, only
hash authentication is dependending on the generator used.

Packed bytes structure:
0: type: str: 4bytesmax
1. Timestamp: int
encrypted with specified mode:
3. app_metadata: arbitrary JSON
\n
data: bytes
"""
from math import floor
from time import time
from base64 import b85encode

from msgpack import packb

from kasten import exceptions

from kasten.types import KastenPacked
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


def pack(data: bytes, data_type: str,
         app_metadata: 'KastenSerializeableDict' = None,
         timestamp: int = None
         ) -> KastenPacked:
    """Create KastenPacked bytes sequence but do not ID or run through generator"""


    # Final data will be:
    # msgpack.packb([data_type, timestamp, {app_metadata}]) \
    # + b'\n' + data
    # Ensure data type does not exceed 4 characters
    if not data_type or len(data_type) > 4:
        raise exceptions.InvalidKastenTypeLength

    try:
        data_type = data_type.decode('utf-8')
    except AttributeError:
        pass

    try:
        data = data.encode('utf-8')
    except AttributeError:
        pass
    if timestamp is None:
        timestamp = floor(time())
    timestamp = int(timestamp)

    kasten_header = [data_type, timestamp, app_metadata]

    kasten_header = b85encode(packb(kasten_header)) + b'\n'
    return kasten_header + data
