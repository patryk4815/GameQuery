import socket
import unicodedata


class Query(object):
    debug = False
    get_other = False

    def query(self, ip, port, typ, timeout=1):
        if hasattr(self, typ):
            return getattr(self, typ)(ip, port, timeout)
        else:
            return None

    def gamespy1(self, ip, port, timeout=1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                s.send(b'\\info\\')
                response = s.recv(1600)

                if self.debug:
                    print(response)
        except:
            return None

        if response.find(b'\\final\\') == -1:
            return None

        list_commands = response[1:].split(b'\\')
        keys = self.__bytelist_to_strlist(list_commands[::2])
        values = list_commands[1::2]
        response = dict(zip(keys, values))

        if self.debug:
            print(response)

        return self.__validate_data(response)

    def gamespy2(self, ip, port, timeout=1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                s.send(b'\xFE\xFD\x00\x43\x4F\x52\x59\xFF\x00\x00')
                response = s.recv(1600)

                if self.debug:
                    print(response)
        except:
            return None

        if response[0:5] != b'\x00CORY':
            return None

        list_commands = response[5:].split(b'\x00\x00\x00')[0].split(b'\x00')
        keys = self.__bytelist_to_strlist(list_commands[::2])
        values = list_commands[1::2]
        response = dict(zip(keys, values))

        if self.debug:
            print(response)

        return self.__validate_data(response)

    def gamespy3(self, ip, port, timeout=1, __challange=False):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))

                challange_int = b''
                timestamp = b'\x04\x05\x06\x07'  # timestamp
                if __challange:
                    s.send(b'\xFE\xFD\x09' + timestamp)
                    response = s.recv(256)

                    if response[:5] != b'\x09' + timestamp:
                        return None

                    challange_int = int(response[5:-1]).to_bytes(4, 'big', signed=True)

                s.send(b'\xFE\xFD\x00' + timestamp + challange_int + b'\xFF\x00\x00\x01')
                response = s.recv(1600)

                if self.debug:
                    print(response)
        except:
            return None

        if response[0] != 0x00 or response[1:5] != timestamp or response[15] != 0x00:
            return None

        list_commands = response[16:-2].split(b'\x00\x00\x01')[0].split(b'\x00')
        try:
            list_commands.remove('p1073741829')  # fix for Unreal Tournament 3 because he have invalid data ?
        except ValueError:
            pass

        keys = self.__bytelist_to_strlist(list_commands[::2])
        values = list_commands[1::2]
        response = dict(zip(keys, values))

        if self.debug:
            print(response)

        return self.__validate_data(response)

    def gamespy4(self, ip, port, timeout=1):
        return self.gamespy3(ip, port, timeout, True)

    def quake3(self, ip, port, timeout=1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                s.send(b'\xFF\xFF\xFF\xFFgetstatus\x0A')
                response = s.recv(1600)

                if self.debug:
                    print(response)
        except:
            return None

        if response[4:19] != b'statusResponse\x0A':
            return None

        list_respond = response[20:].split(b'\x0A')
        list_commands = list_respond[0].split(b'\\')
        list_players = list_respond[1:-1]

        keys = self.__bytelist_to_strlist(list_commands[::2])
        values = list_commands[1::2]
        response = dict(zip(keys, values))

        response['q_players'] = len(list_players)

        if self.debug:
            print(response)

        return self.__validate_data(response)

    def valve(self, ip, port, timeout=1):
        Query._end_pointer = 0

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))
                s.send(b'\xFF\xFF\xFF\xFF\x54Source Engine Query\x00')
                response = s.recv(1600)

                if self.debug:
                    print(response)
        except:
            return None

        if response[0:4] != b'\xFF\xFF\xFF\xFF' or (response[4] != 109 and response[4] != 73):
            return None

        response = response[4:]

        response_data = dict()
        response_data['header'] = self.__next_pointer_data(response, 'byte')

        if response_data['header'] == 109:  # old (goldsource)

            response_data['address'] = self.__next_pointer_data(response, 'string')
            response_data['q_hostname'] = self.__next_pointer_data(response, 'string')
            response_data['q_map'] = self.__next_pointer_data(response, 'string')
            response_data['folder'] = self.__next_pointer_data(response, 'string')
            response_data['game'] = self.__next_pointer_data(response, 'string')
            response_data['q_players'] = self.__next_pointer_data(response, 'byte')
            response_data['q_maxplayers'] = self.__next_pointer_data(response, 'byte')
            response_data['protocol'] = self.__next_pointer_data(response, 'byte')
            response_data['server_type'] = self.__next_pointer_data(response, 'byte')
            response_data['environment'] = self.__next_pointer_data(response, 'byte')
            response_data['q_password'] = self.__next_pointer_data(response, 'byte')

            response_data['mod'] = self.__next_pointer_data(response, 'byte')
            if response_data['mod'] == 1:
                response_data['link'] = self.__next_pointer_data(response, 'string')
                response_data['download_link'] = self.__next_pointer_data(response, 'string')
                self.__next_pointer_data(response, 'byte')  # null byte
                response_data['version'] = self.__next_pointer_data(response, 'long')
                response_data['size'] = self.__next_pointer_data(response, 'long')
                response_data['type'] = self.__next_pointer_data(response, 'byte')
                response_data['dll'] = self.__next_pointer_data(response, 'byte')

            response_data['vac'] = self.__next_pointer_data(response, 'byte')
            response_data['bots'] = self.__next_pointer_data(response, 'byte')

        else:  # new (source) 73

            response_data['protocol'] = self.__next_pointer_data(response, 'byte')
            response_data['q_hostname'] = self.__next_pointer_data(response, 'string')
            response_data['q_map'] = self.__next_pointer_data(response, 'string')
            response_data['folder'] = self.__next_pointer_data(response, 'string')
            response_data['game'] = self.__next_pointer_data(response, 'string')
            response_data['appid'] = self.__next_pointer_data(response, 'short')
            response_data['q_players'] = self.__next_pointer_data(response, 'byte')
            response_data['q_maxplayers'] = self.__next_pointer_data(response, 'byte')
            response_data['bots'] = self.__next_pointer_data(response, 'byte')
            response_data['server_type'] = self.__next_pointer_data(response, 'byte')
            response_data['environment'] = self.__next_pointer_data(response, 'byte')
            response_data['q_password'] = self.__next_pointer_data(response, 'byte')
            response_data['vac'] = self.__next_pointer_data(response, 'byte')

            #the ship
            if response_data['appid'] == 2400:
                response_data['mode'] = self.__next_pointer_data(response, 'byte')
                response_data['witnesses'] = self.__next_pointer_data(response, 'byte')
                response_data['duration'] = self.__next_pointer_data(response, 'byte')

            response_data['version'] = self.__next_pointer_data(response, 'string')

            response_data['edf'] = self.__next_pointer_data(response, 'byte')
            if response_data['edf'] > 0:
                if response_data['edf'] & 0x80:
                    response_data['gameport'] = self.__next_pointer_data(response, 'short')

                if response_data['edf'] & 0x10:
                    response_data['steamID'] = self.__next_pointer_data(response, 'longlong')

                if response_data['edf'] & 0x40:
                    response_data['tv_port'] = self.__next_pointer_data(response, 'short')
                    response_data['tv_name'] = self.__next_pointer_data(response, 'string')

                if response_data['edf'] & 0x20:
                    response_data['tags'] = self.__next_pointer_data(response, 'string')

                if response_data['edf'] & 0x01:
                    response_data['gameID'] = self.__next_pointer_data(response, 'longlong')

                    # fix for Just Cause 2, because he have in mapname our info for players and maxplayers
                    if response_data['gameID'] == 259080 and response_data['q_map'][0:9] == b'Players: ':
                        parse_data = response_data['q_map'][9:].split(b'/')

                        response_data['q_maxplayers'] = self.__any_to_bytes(parse_data[1])
                        response_data['q_players'] = self.__any_to_bytes(parse_data[0])
                        response_data['q_map'] = b''

        if self.debug:
            print(response_data)

        return self.__validate_data(response_data)

    @staticmethod
    def __any_to_bytes(data):
        if type(data) in (int, float):
            return str(data).encode()
        elif type(data) == str:
            return data.encode()
        else:
            return data

    @staticmethod
    def __bytes_to_str(string_bytes):
        try:
            string_bytes = string_bytes.decode('utf-8')
        except UnicodeError:
            string_bytes = string_bytes.decode('latin-1', errors='ignore')

        string_bytes = unicodedata.normalize('NFKD', string_bytes)
        # string_bytes = string_bytes.replace('\u00A0', ' ')  # replace non-break space to normal space
        return string_bytes

    @staticmethod
    def __bytelist_to_strlist(bytelist):
        return [Query.__bytes_to_str(x) for x in bytelist]

    @staticmethod
    def __no_hostname(dictionary, key):
        if key not in dictionary or not dictionary[key]:
            return '-- Unnamed --'

        return Query.__bytes_to_str(dictionary[key])

    @staticmethod
    def __no_mapname(dictionary, key):
        if key not in dictionary or not dictionary[key]:
            return 'Unknown'

        return Query.__bytes_to_str(dictionary[key])

    @staticmethod
    def __no_password(dictionary, key):
        if key not in dictionary or not dictionary[key]:
            return False

        return False if dictionary[key].lower() in [b'false', b'0'] else True

    @staticmethod
    def __no_int(dictionary, key):
        if key not in dictionary or not dictionary[key]:
            return 0

        if type(dictionary[key]) == int:
            return dictionary[key]

        return int(dictionary[key])

    @staticmethod
    def __normalize_data(response):
        response = response.copy()
        dict_normalize = {
            'q_hostname': ['hostname', 'sv_hostname'],
            'q_map': ['p1073741825', 'mapname', 'map'],
            'q_players': ['numplayers'],
            'q_maxplayers': ['maxplayers', 'sv_maxclients'],
            'q_password': ['password', 'g_needpass', 'pswrd'],
        }

        for key, value in dict_normalize.items():
            for x in value:
                if x in response:
                    response[key] = response[x]
                    response.pop(x)
                    break

        return response

    def __validate_data(self, response):
        response = self.__normalize_data(response)
        info = dict()
        info['hostname'] = self.__no_hostname(response, 'q_hostname')
        info['map'] = self.__no_mapname(response, 'q_map')
        info['players'] = self.__no_int(response, 'q_players')
        info['maxplayers'] = self.__no_int(response, 'q_maxplayers')
        info['is_password'] = self.__no_password(response, 'q_password')

        if self.get_other:
            try:
                response.pop('q_hostname')
                response.pop('q_map')
                response.pop('q_maxplayers')
                response.pop('q_password')
            except:
                pass

            info.update(response)

        # if info['players'] > info['maxplayers']:
        #     info['players'] = info['maxplayers']
        return info

    @staticmethod
    def __next_pointer_data(data, typ):
        start_pointer = Query._end_pointer

        if typ == 'string':
            try:
                Query._end_pointer = data.index(b'\x00', start_pointer) + 1  # +1 because it need to get \x00 byte
            except ValueError:
                return b''  # if next null byte not found, then return empty string

            return data[start_pointer:Query._end_pointer - 1]
        elif typ == 'byte':
            Query._end_pointer += 1
            return int.from_bytes(data[start_pointer:Query._end_pointer], 'little')
        elif typ == 'short':
            Query._end_pointer += 2
            return int.from_bytes(data[start_pointer:Query._end_pointer], 'little')
        elif typ == 'long':
            Query._end_pointer += 4
            return int.from_bytes(data[start_pointer:Query._end_pointer], 'little')
        elif typ == 'longlong':
            Query._end_pointer += 8
            return int.from_bytes(data[start_pointer:Query._end_pointer], 'little')
        else:
            return None
