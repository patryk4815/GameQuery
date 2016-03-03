from query.protocols import _Base

__author__ = 'Patryk'


class Gamespy3(_Base):
    def __init__(self, ip, port, timeout=1, _challange=False):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))

                challange_int = b''
                timestamp = b'\x04\x05\x06\x07'  # timestamp
                if _challange:
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

