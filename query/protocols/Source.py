import logging
import asyncio
from . import BaseUDP
from ..parser.helpers import QueryBytes
from ..connection import Timeout


class Source(BaseUDP):
    A2S_HEADER = -1
    A2S_REQUEST_CHALLENGE = -1
    A2S_RESPONSE_CHALLENGE = ord('A')
    A2S_INFO = ord('T')
    A2S_RESPONSE_INFO = ord('I')
    A2S_RESPONSE_INFO_OLD = ord('m')

    A2S_PLAYER = ord('U')
    A2S_RESPONSE_PLAYER = ord('D')

    A2S_RULES = ord('V')

    async def get_info(self):
        try:
            with Timeout(self._timeout):
                reader, writer = await self._connection.connect()

                query = QueryBytes()
                query.append(self.A2S_HEADER, QueryBytes.LITTLE_TYPE_INT)
                query.append(self.A2S_INFO, QueryBytes.LITTLE_TYPE_CHAR)
                query.append('Source Engine Query', QueryBytes.TYPE_STRING)

                writer.write(query.buffer)
                return self.parse_get_info(await reader.readline())
        except asyncio.TimeoutError:
            return None

    async def get_players(self):
        try:
            with Timeout(self._timeout):
                reader, writer = await self._connection.connect()

                query = QueryBytes()
                query.append(self.A2S_HEADER, QueryBytes.LITTLE_TYPE_INT)
                query.append(self.A2S_PLAYER, QueryBytes.LITTLE_TYPE_CHAR)
                query.append(self.A2S_REQUEST_CHALLENGE, QueryBytes.LITTLE_TYPE_INT)

                writer.write(query.buffer)
                challenge_code = self.parse_challenge(await reader.readline())

                query.replace(challenge_code, QueryBytes.LITTLE_TYPE_INT, offset=5)
                writer.write(query.buffer)
                return self.parse_players(await reader.readline())
        except asyncio.TimeoutError:
            return None

    def parse_players(self, response):
        logging.critical(response)  # fixme

        response = QueryBytes(response)
        if response.pop(QueryBytes.LITTLE_TYPE_INT) != self.A2S_HEADER:
            return []

        if response.pop(QueryBytes.LITTLE_TYPE_CHAR) != self.A2S_RESPONSE_PLAYER:
            return []

        players_num = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        list_players = list()
        for i in range(0, players_num):
            index = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            name = response.pop(QueryBytes.TYPE_STRING)
            score = response.pop(QueryBytes.LITTLE_TYPE_LONG)
            duration = response.pop(QueryBytes.LITTLE_TYPE_FLOAT)
            list_players.append({
                'name': name,
                'score': score,
                'duration': duration,
            })
        return list_players

    def parse_challenge(self, response):
        logging.critical(response)  # fixme

        response = QueryBytes(response)
        if response.pop(QueryBytes.LITTLE_TYPE_INT) == self.A2S_HEADER:
            if response.pop(QueryBytes.LITTLE_TYPE_CHAR) == self.A2S_RESPONSE_CHALLENGE:
                return response.pop(QueryBytes.LITTLE_TYPE_INT)
        raise ValueError('MALFORMED')

    def parse_get_info(self, response):
        logging.critical(response)  # fixme

        response = QueryBytes(response)
        if response.pop(QueryBytes.LITTLE_TYPE_INT) != self.A2S_HEADER:
            return None

        header = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
        if header not in (self.A2S_RESPONSE_INFO, self.A2S_RESPONSE_INFO_OLD):
            return None

        response_data = dict()
        response_data['header'] = header

        if header == self.A2S_RESPONSE_INFO_OLD:  # old (goldsource)
            response_data['address'] = response.pop(QueryBytes.TYPE_STRING)
            response_data['hostname'] = response.pop(QueryBytes.TYPE_STRING)
            response_data['map'] = response.pop(QueryBytes.TYPE_STRING)
            response_data['folder'] = response.pop(QueryBytes.TYPE_STRING)
            response_data['game'] = response.pop(QueryBytes.TYPE_STRING)
            response_data['players'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['maxplayers'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['protocol'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['server_type'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['environment'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['password'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)

            response_data['mod'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            if response_data['mod'] == 0x01:
                response_data['link'] = response.pop(QueryBytes.TYPE_STRING)
                response_data['download_link'] = response.pop(QueryBytes.TYPE_STRING)

                response.pop(QueryBytes.LITTLE_TYPE_BYTE)  # null byte

                response_data['version'] = response.pop(QueryBytes.LITTLE_TYPE_LONG)
                response_data['size'] = response.pop(QueryBytes.LITTLE_TYPE_LONG)
                response_data['type'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
                response_data['dll'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)

            response_data['vac'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['bots'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)

        elif header == self.A2S_RESPONSE_INFO:  # new (source) 73

            response_data['protocol'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['hostname'] = response.pop(QueryBytes.TYPE_STRING)
            response_data['map'] = response.pop(QueryBytes.TYPE_STRING)
            response_data['folder'] = response.pop(QueryBytes.TYPE_STRING)
            response_data['game'] = response.pop(QueryBytes.TYPE_STRING)
            response_data['appid'] = response.pop(QueryBytes.LITTLE_TYPE_SHORT)
            response_data['players'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['maxplayers'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['bots'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['server_type'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['environment'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['password'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            response_data['vac'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)

            #the ship
            if response_data['appid'] == 2400:
                response_data['mode'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
                response_data['witnesses'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
                response_data['duration'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)

            response_data['version'] = response.pop(QueryBytes.TYPE_STRING)

            response_data['edf'] = response.pop(QueryBytes.LITTLE_TYPE_CHAR)
            if response_data['edf'] > 0:
                if response_data['edf'] & 0x80:
                    response_data['gameport'] = response.pop(QueryBytes.LITTLE_TYPE_SHORT)

                if response_data['edf'] & 0x10:
                    response_data['steamID'] = response.pop(QueryBytes.LITTLE_TYPE_LONGLONG)

                if response_data['edf'] & 0x40:
                    response_data['tv_port'] = response.pop(QueryBytes.LITTLE_TYPE_SHORT)
                    response_data['tv_name'] = response.pop(QueryBytes.TYPE_STRING)

                if response_data['edf'] & 0x20:
                    response_data['tags'] = response.pop(QueryBytes.TYPE_STRING)

                if response_data['edf'] & 0x01:
                    response_data['gameID'] = response.pop(QueryBytes.LITTLE_TYPE_LONGLONG)

                    # fix for Just Cause 2, because he have in mapname our info for players and maxplayers
                    # if response_data['gameID'] == 259080 and response_data['q_map'][0:9] == b'Players: ':
                    #     parse_data = response_data['q_map'][9:].split(b'/')
                    #
                    #     response_data['q_maxplayers'] = self._any_to_bytes(parse_data[1])
                    #     response_data['q_players'] = self._any_to_bytes(parse_data[0])
                    #     response_data['q_map'] = b''

        return response_data
