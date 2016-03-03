from query.protocols import _Base

__author__ = 'Patryk'


class Gamespy1(_Base):
    def __init__(self, ip, port, timeout=1):
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

