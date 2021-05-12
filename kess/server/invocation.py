from typing import Dict

from fastapi import APIRouter
from kess.server import module

OPTIONS_KEY = "__invocation_options__"


class InvocationMethod:
    def __call__(self, path: str = ""):
        return self.put(path)

    def wrap(self, path: str, method: str):
        def _wrapper(func: module.ModuleFunction):
            setattr(func, OPTIONS_KEY, {"method": method, "path": path})
            return func

        return _wrapper

    def get(self, path: str = ""):
        return self.wrap(path, "GET")

    def post(self, path: str = ""):
        return self.wrap(path, "POST")

    def put(self, path: str = ""):
        return self.wrap(path, "PUT")

    def update(self, path: str = ""):
        return self.wrap(path, "UPDATE")

    def delete(self, path: str = ""):
        return self.wrap(path, "DELETE")


m = method = InvocationMethod()


def create(obj: module.Module, name: str = None) -> APIRouter:
    return create_router_from_dict({k: getattr(obj, k) for k in dir(obj)}, name=name)


def create_router_from_dict(obj: Dict, name: str) -> APIRouter:
    router = APIRouter(prefix=f"/{name}", tags=[name])
    for k, v in obj.items():
        if not k.startswith("_") and callable(v) and hasattr(v, OPTIONS_KEY):
            opts = getattr(v, OPTIONS_KEY)
            router.add_api_route(
                opts["path"],
                v,
                methods=[opts["method"]],
                summary=v.__name__,
            )
    return router
