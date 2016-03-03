import sys

if sys.version_info < (3, 5):
    raise RuntimeError('You need Python 3.5+ for this module.')

# from .protocols.Source import Source
#
# from query.protocols import Source
#
#
# class Query(object):
#     def query(self, ip, port, typ, timeout=1):
#         if typ != 'source':
#             return None
#         obj = Source.Source()
#         return getattr(obj, 'get_info')(ip, port, timeout)
#
# __all__ = [
#     'Query'
# ]