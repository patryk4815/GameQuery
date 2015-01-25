import sys

if sys.version_info < (3, 4):
    raise RuntimeError('You need Python 3.4+ for this module.')

from query.query import Query

__all__ = [
    'Query'
]