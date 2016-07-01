from .connection import Timeout

__all__ = (
    'async_raise_on_timeout',
)


def async_raise_on_timeout(*args0, property_name='_timeout'):
    if args0:
        func = args0[0]
        async def _inner(self, *args, **kwargs):
            with Timeout(getattr(self, property_name, 600)):
                return await func(self, *args, **kwargs)
        return _inner
    else:
        def _wrap(*args1):
            func = args1[0]
            async def _inner(self, *args, **kwargs):
                with Timeout(getattr(self, property_name, 600)):
                    return await func(self, *args, **kwargs)
            return _inner
        return _wrap
