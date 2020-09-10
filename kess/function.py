from typing import Callable

from fastapi import FastAPI


class Function(FastAPI):
    def handle(self, fn) -> Callable:
        return self.post("/")(fn)

    def h(self, fn) -> Callable:
        return self.handle(fn)
