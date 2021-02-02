import asyncio
from concurrent.futures import process

_executor = None


def executor(*args, **kwargs) -> process.ProcessPoolExecutor:
    global _executor
    if not _executor:
        _executor = process.ProcessPoolExecutor(*args, **kwargs)
    return _executor


async def run_in_executor(executor, *args, **kwargs):
    return await asyncio.get_event_loop().run_in_executor(executor, *args, **kwargs)


async def run_in_process(*args, **kwargs):
    return await run_in_executor(executor(), *args, **kwargs)
