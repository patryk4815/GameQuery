from query.protocols import _Base

__author__ = 'Patryk'

class Quake3(_Base):
    def __init__(self, ip, port, timeout=1):
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
