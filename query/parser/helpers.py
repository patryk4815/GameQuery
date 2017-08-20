import struct
import unicodedata

__all__ = [
    'QueryBytes',
]


class BytesTypeByte(object):
    def _pack(self, data):
        if isinstance(data, str):
            data = data.encode()
        return data + b'\x00'  # fixme?

    def _unpack(self, data: bytes):
        end_cursor = data.find(b'\x00')
        if end_cursor == -1:
            return bytes(data[:]), len(data)  # get all to end

        return bytes(data[:end_cursor]), end_cursor + 1

    def pack(self, data):
        parsed = self._pack(data)
        return parsed, len(parsed)

    def unpack(self, data: bytes, offset=None):
        parsed, size = self._unpack(data[offset:])
        return parsed, size


class BytesTypeString(BytesTypeByte):
    def unpack(self, data: bytes, offset=None):
        parsed, size = super().unpack(data, offset=offset)

        try:
            parsed = parsed.decode('utf-8')
        except UnicodeError:
            parsed = parsed.decode('latin-1', errors='ignore')

        parsed = unicodedata.normalize('NFKD', parsed)
        return parsed, size


class BytesTypeC(object):
    def __init__(self, c_type):
        self._c_type = c_type
        self._size = struct.calcsize(self._c_type)

    @property
    def size(self):
        return self._size

    def unpack(self, data: bytes, offset=None):
        size = self._size
        if offset is not None:
            size += offset

        return struct.unpack(self._c_type, data[offset:size])[0], self._size

    def pack(self, data: bytes):
        return struct.pack(self._c_type, data), self._size


class QueryBytes(object):
    # little-endian "<"
    LITTLE_TYPE_BYTE = BytesTypeC('<c')  # 1 - byte
    BIG_TYPE_BYTE = BytesTypeC('>c')  # 1 - byte

    LITTLE_TYPE_CHAR = BytesTypeC('<b')  # 1 - int
    LITTLE_TYPE_uCHAR = BytesTypeC('<B')  # 1 - int

    BIG_TYPE_CHAR = BytesTypeC('>b')  # 1 - int
    BIG_TYPE_uCHAR = BytesTypeC('>B')  # 1 - int

    LITTLE_TYPE_SHORT = BytesTypeC('<h')  # 2 - int
    LITTLE_TYPE_uSHORT = BytesTypeC('<H')  # 2 - int

    BIG_TYPE_SHORT = BytesTypeC('>h')  # 2 - int
    BIG_TYPE_uSHORT = BytesTypeC('>H')  # 2 - int

    LITTLE_TYPE_INT = BytesTypeC('<i')  # 4 - int
    LITTLE_TYPE_uINT = BytesTypeC('<I')  # 4 - int

    BIG_TYPE_INT = BytesTypeC('>i')  # 4 - int
    BIG_TYPE_uINT = BytesTypeC('>I')  # 4 - int

    LITTLE_TYPE_LONG = BytesTypeC('<l')  # 4 - int
    LITTLE_TYPE_uLONG = BytesTypeC('<L')  # 4 - int

    BIG_TYPE_LONG = BytesTypeC('>l')  # 4 - int
    BIG_TYPE_uLONG = BytesTypeC('>L')  # 4 - int

    LITTLE_TYPE_LONGLONG = BytesTypeC('<q')  # 8 - int
    LITTLE_TYPE_uLONGLONG = BytesTypeC('<Q')  # 8 - int

    BIG_TYPE_LONGLONG = BytesTypeC('>q')  # 8 - int
    BIG_TYPE_uLONGLONG = BytesTypeC('>Q')  # 8 - int

    LITTLE_TYPE_FLOAT = BytesTypeC('<f')  # 4 - float
    LITTLE_TYPE_DOUBLE = BytesTypeC('<d')  # 8 - float

    BIG_TYPE_FLOAT = BytesTypeC('>f')  # 4 - float
    BIG_TYPE_DOUBLE = BytesTypeC('>d')  # 8 - float

    TYPE_BYTE = BytesTypeByte()  # parse to null byte
    TYPE_STRING = BytesTypeString()  # parse to null byte

    def __init__(self, buffer=None):
        self._buffer = bytearray(buffer) if buffer else bytearray()
        self._cursor = 0

    def __str__(self):
        return str(self._buffer)

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, index):
        if index > len(self._buffer):
            raise ValueError('index too big then buffer')

        self._cursor = index

    @property
    def buffer(self):
        return bytes(self._buffer[:])

    def _unpack_data(self, c_type, offset=None):
        if offset is None:
            offset = self._cursor

        if isinstance(c_type, (list, tuple)):
            base_offset = offset
            list_data = list()
            for c_type_lo in c_type:
                data, size = c_type_lo.unpack(self._buffer, offset=offset)
                list_data.append(data)
                offset += size

            return list_data, offset - base_offset

        return c_type.unpack(self._buffer, offset=offset)

    def _pack_data(self, data, c_type):
        return c_type.pack(data)

    def get(self, c_type, change_cursor=True, offset=None):
        data, size = self._unpack_data(c_type, offset)
        if change_cursor:
            self._cursor += size

        return data

    def pop(self, c_type, offset=None):
        data, size = self._unpack_data(c_type, offset)
        del self._buffer[self._cursor:self._cursor + size]

        return data

    def _set(self, data, c_type, offset=None, size=None,):
        if offset is None:
            offset = self._cursor

        data, size_c = self._pack_data(data, c_type)
        if size is None:
            size = size_c

        self._buffer[offset:offset + size] = data
        return offset + size

    def set(self, data, c_type, size, offset=None):
        return self._set(data, c_type, size=size, offset=offset)

    def replace(self, data, c_type, offset=None):
        return self._set(data, c_type, size=None, offset=offset)

    def append(self, data, c_type):
        if c_type is None:
            assert isinstance(data, bytes)
        else:
            data, size = self._pack_data(data, c_type)
        self._buffer.extend(data)
