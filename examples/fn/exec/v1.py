from typing import Any, List, Optional

from kess import Function, asyncio, method
from pydantic import BaseModel


class Cache:
    def __init__(self, funcname: str = "main"):
        self._cache = {}
        self._funcname = funcname

    def has(self, key: str) -> bool:
        return key in self._cache

    def get(self, key: str, default=None) -> Any:
        _main = self._cache.get(key)
        if not _main and default:
            _main = self.set(key, default)
        return _main

    def set(self, key: str, func: str) -> Any:
        _main = self._exec(func)
        if not _main:
            raise Exception("No main func")
        if key:
            self._cache[key] = _main
        return _main

    def pop(self, key: str) -> None:
        return self._cache.pop(key)

    def clear(self):
        self._cache = {}

    def _exec(self, func: str) -> Any:
        _locals = {}
        exec(func, globals(), _locals)
        return _locals.get(self._funcname)


class Options(BaseModel):
    key: Optional[str] = None
    type: Optional[str] = None
    func: Optional[str] = None
    force: Optional[bool] = False
    args: Optional[List] = []


class Manager:
    cache: Cache

    def __init__(self):
        self.cache = Cache()

    async def run(self, opts: Options) -> Any:
        _main = None
        if opts.force:
            _main = self.cache.set(opts.key, opts.func)
        else:
            _main = self.cache.get(opts.key, opts.func)
        if not _main:
            raise Exception("Require main function")

        if opts.type == "process":
            return await asyncio.run_in_process(_main, *opts.args)
        elif opts.type == "asyncio":
            return await _main(*opts.args)
        else:
            return _main(*opts.args)


class ExecV1(Function):
    manager = Manager()

    @method
    async def execrun(self, opts: Options) -> Any:
        return await self.manager.run(opts)
