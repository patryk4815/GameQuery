from query.protocols import _Base

__author__ = 'Patryk'


class Gamespy2(_Base):
    def __init__(self, ip, port, timeout=1):
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

