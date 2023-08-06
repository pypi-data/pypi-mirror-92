"""Main Kasten object, does nothing but provide access to packed Kasten bytes and call a specified generator function"""
from base64 import b85decode

from msgpack import unpackb
import msgpack

from .types import KastenChecksum
from .types import KastenPacked
from .generator import pack
from .exceptions import InvalidPackedBytes
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

class Kasten:
    def __init__(self,
                 id: KastenChecksum,
                 packed_bytes: KastenPacked,
                 generator: 'KastenBaseGenerator',  # noqa
                 *additional_generator_args,
                 auto_check_generator=True,
                 **additional_generator_kwargs):  # noqa
        self.id = id
        self.generator = generator
        try:
            header, data = packed_bytes.split(b'\n', 1)
        except ValueError:
            raise InvalidPackedBytes("Could not extract data section")
        header = b85decode(header)
        try:
            header = unpackb(
                header,
                strict_map_key=True)
        except(  # noqa
                msgpack.exceptions.ExtraData,
                msgpack.FormatError,
                UnicodeEncodeError,
                ValueError) as _:
            raise InvalidPackedBytes("Could not decode packed bytes")
        self.header = header
        self.data = data
        self.additional_generator_args = list(additional_generator_args)
        self.additional_generator_kwargs = dict(additional_generator_kwargs)
        int(self.get_timestamp())
        if auto_check_generator:
            self.check_generator()

    def check_generator(self, generator=None):
        packed = self.get_packed()
        if generator is None:
            self.generator.validate_id(
                self.id, packed,
                *self.additional_generator_args,
                **self.additional_generator_kwargs)
        else:
            generator(self.id, packed)

    # Getters are gross, but they are used here to preserve space

    def get_packed(self) -> KastenPacked:
        def _get_or_none(func):
            try:
                ret = func()
            except IndexError:
                return None
            except TypeError:
                return None
            return ret
        return pack.pack(self.data, self.get_data_type(),
                         app_metadata=_get_or_none(self.get_metadata),
                         timestamp=self.get_timestamp())

    def get_data_type(self) -> str: return self.header[0]

    def get_timestamp(self): return self.header[1]

    def get_metadata(self): return self.header[2]
