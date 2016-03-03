from query.protocols import _Base
from query.protocols.Gamespy3 import Gamespy3

__author__ = 'Patryk'


class Gamespy4(_Base, Gamespy3):
    def __init__(self, ip, port, timeout=1):
        return Gamespy3.__init__(ip, port, timeout, True)
