from typing import Callable, Dict

from fastapi import FastAPI


class Function:
    name: str
    version: str
    app: FastAPI

    def __init__(self):
        self.app = FastAPI()
        self.name = None
        self.version = "latest"

    def __call__(self, fn=None, **kwargs) -> Callable:
        register = self.post("/", **kwargs)
        return register(fn) if fn else register

    def setup(self, name: str, version: str = "latest"):
        self.name = name
        self.version = version

    def prefix(self) -> str:
        return f"/{self.name}/{self.version}"

    def docs_path(self) -> str:
        return f"{self.prefix()}/docs"

    def _kwargs(self, kwargs: Dict) -> Dict:
        # kwargs.setdefault("tags", [self.name])
        return kwargs

    def get(self, path: str, **kwargs) -> Callable:
        return self.app.get(path, **self._kwargs(kwargs))

    def post(self, path: str, **kwargs) -> Callable:
        return self.app.post(path, **self._kwargs(kwargs))

    def update(self, path: str, **kwargs) -> Callable:
        return self.app.update(path, **self._kwargs(kwargs))

    def patch(self, path: str, **kwargs) -> Callable:
        kwargs.setdefault("tags", [self.name])
        return self.app.patch(path, **self._kwargs(kwargs))

    def delete(self, path: str, **kwargs) -> Callable:
        return self.app.delete(path, **self._kwargs(kwargs))
