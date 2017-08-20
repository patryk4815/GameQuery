import asyncio

__all__ = [
    'open_connection',
]

async def open_connection(*args, **kwargs):
    return asyncio.open_connection(*args, **kwargs)
