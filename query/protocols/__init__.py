import asyncio
from ..connection import open_datagram_connection, open_connection


class Base(object):
    def __init__(self, *, ip, port, timeout, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()

        self._ip = ip
        self._port = port
        self._timeout = timeout
        self._loop = loop


class UDPConnector(Base):
    def __init__(self, *, ip, port, timeout, loop=None):
        super().__init__(ip=ip, port=port, timeout=timeout, loop=loop)
        self._is_closed = False
        self._conns = list()

    async def connect(self):
        args = await open_datagram_connection(
            self._ip,
            self._port,
            timeout_connection=self._timeout,
            loop=self._loop
        )
        self._conns.append(args)
        return args

    def close(self):
        if self._is_closed:
            return

        self._is_closed = True
        for reader, writer in self._conns:
            writer.close()


class BaseUDP(Base):
    def __init__(self, *, ip, port, timeout, loop=None):
        super().__init__(ip=ip, port=port, timeout=timeout, loop=loop)
        self._connection = UDPConnector(ip=ip, port=port, timeout=timeout, loop=loop)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()


class BaseTCP(Base):
    pass

# class Base(object):
#     def __init__(self):
#         self._end_pointer = 0
#         self.get_other = False
#
#     @staticmethod
#     def _any_to_bytes(data):
#         if isinstance(data, bytes):
#             return data
#
#         if isinstance(data, (int, float)):
#             return str(data).encode()
#         elif isinstance(data, str):
#             return data.encode()
#
#         raise AttributeError('data is not str, int, float or bytes: {}'.format(data))
#
#     @staticmethod
#     def _bytes_to_str(string_bytes):
#         try:
#             string_bytes = string_bytes.decode('utf-8')
#         except UnicodeError:
#             string_bytes = string_bytes.decode('latin-1', errors='ignore')
#
#         return unicodedata.normalize('NFKD', string_bytes)
#
#     @classmethod
#     def _bytelist_to_strlist(cls, bytelist):
#         return [cls._bytes_to_str(data) for data in bytelist]
#
#     @classmethod
#     def _no_hostname(cls, dictionary, key):
#         if key not in dictionary or not dictionary[key]:
#             return '-- Unnamed --'
#
#         return cls._bytes_to_str(dictionary[key])
#
#     @classmethod
#     def _no_mapname(cls, dictionary, key):
#         if key not in dictionary or not dictionary[key]:
#             return 'Unknown'
#
#         return cls._bytes_to_str(dictionary[key])
#
#     @staticmethod
#     def _no_password(dictionary, key):
#         if key not in dictionary or not dictionary[key]:
#             return False
#
#         return False if dictionary[key].lower() in [b'false', b'0'] else True
#
#     @staticmethod
#     def _no_int(dictionary, key):
#         if key not in dictionary or not dictionary[key]:
#             return 0
#
#         if type(dictionary[key]) == int:
#             return dictionary[key]
#
#         return int(dictionary[key])
#
#     @staticmethod
#     def _normalize_data(response):
#         response = response.copy()
#         dict_normalize = {
#             'q_hostname': ['hostname', 'sv_hostname'],
#             'q_map': ['p1073741825', 'mapname', 'map'],
#             'q_players': ['numplayers'],
#             'q_maxplayers': ['maxplayers', 'sv_maxclients'],
#             'q_password': ['password', 'g_needpass', 'pswrd'],
#         }
#
#         for key, value in dict_normalize.items():
#             for x in value:
#                 if x in response:
#                     response[key] = response[x]
#                     response.pop(x)
#                     break
#
#         return response
#
#     def _validate_data(self, response):
#         response = self._normalize_data(response)
#         info = dict()
#         info['hostname'] = self._no_hostname(response, 'q_hostname')
#         info['map'] = self._no_mapname(response, 'q_map')
#         info['players'] = self._no_int(response, 'q_players')
#         info['maxplayers'] = self._no_int(response, 'q_maxplayers')
#         info['is_password'] = self._no_password(response, 'q_password')
#
#         if self.get_other:
#             try:
#                 response.pop('q_hostname')
#                 response.pop('q_map')
#                 response.pop('q_maxplayers')
#                 response.pop('q_password')
#             except:
#                 pass
#
#             info.update(response)
#
#         # if info['players'] > info['maxplayers']:
#         #     info['players'] = info['maxplayers']
#         return info
#
#     def _next_pointer_data(self, data, type_):
#         start_pointer = self._end_pointer
#
#         if type_ == 'string':
#             try:
#                 self._end_pointer = data.index(b'\x00', start_pointer) + 1  # +1 because it need to get \x00 byte
#             except ValueError:
#                 return b''  # if next null byte not found, then return empty string
#
#             return data[start_pointer:self._end_pointer - 1]
#         elif type_ == 'byte':
#             self._end_pointer += 1
#             return int.from_bytes(data[start_pointer:self._end_pointer], 'little')
#         elif type_ == 'short':
#             self._end_pointer += 2
#             return int.from_bytes(data[start_pointer:self._end_pointer], 'little')
#         elif type_ == 'long':
#             self._end_pointer += 4
#             return int.from_bytes(data[start_pointer:self._end_pointer], 'little')
#         elif type_ == 'longlong':
#             self._end_pointer += 8
#             return int.from_bytes(data[start_pointer:self._end_pointer], 'little')
#         else:
#             return None
#
#
# # from query.query import Query
#
#
# # __all__ = [
# #     'Query'
# # ]
