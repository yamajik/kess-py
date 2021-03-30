from typing import Callable, Dict, Type, Union

from fastapi import APIRouter
import dapr


class Invocation:
    ...


class InvocationMethod:
    def __call__(self, func_or_path: Union[Callable, str]):
        return self.put(func_or_path)

    def wrap(self, func: Callable, method: str = "PUT", path: str = ""):
        func.__invocationmethod__ = method
        func.__invocationpath__ = path
        return func

    def get(self, func_or_path: Union[Callable, str]):
        if callable(func_or_path):
            return self.wrap(func_or_path, method="GET")

        def wrapper(funcobj):
            return self.wrap(funcobj, method="GET", path=f"/{func_or_path}")

        return wrapper

    def post(self, func_or_path: Union[Callable, str]):
        if callable(func_or_path):
            return self.wrap(func_or_path, method="POST")

        def wrapper(funcobj):
            return self.wrap(funcobj, method="POST", path=f"/{func_or_path}")

        return wrapper

    def put(self, func_or_path: Union[Callable, str]):
        if callable(func_or_path):
            return self.wrap(func_or_path, method="PUT")

        def wrapper(funcobj):
            return self.wrap(funcobj, method="PUT", path=f"/{func_or_path}")

        return wrapper

    def update(self, func_or_path: Union[Callable, str]):
        if callable(func_or_path):
            return self.wrap(func_or_path, method="UPDATE")

        def wrapper(funcobj):
            return self.wrap(funcobj, method="UPDATE", path=f"/{func_or_path}")

        return wrapper

    def delete(self, func_or_path: Union[Callable, str]):
        if callable(func_or_path):
            return self.wrap(func_or_path, method="DELETE")

        def wrapper(funcobj):
            return self.wrap(funcobj, method="DELETE", path=f"/{func_or_path}")

        return wrapper


m = method = InvocationMethod()


def create(obj: Type[Invocation], name: str = None) -> APIRouter:
    return create_router(obj(), name=name or obj.__name__)


def create_from_dict(obj: Dict, name: str) -> APIRouter:
    return create_router_from_dict(obj, name=name)


def create_router(obj: Invocation, name: str = None) -> APIRouter:
    return create_router_from_dict(
        {k: getattr(obj, k) for k in dir(obj)}, name or obj.__name__
    )


def create_router_from_dict(obj: Dict, name: str) -> APIRouter:
    router = APIRouter(prefix=f"/{name}", tags=[name])
    for k, v in obj.items():
        if not k.startswith("_") and callable(v) and hasattr(v, "__invocationmethod__"):
            router.add_api_route(
                getattr(v, "__invocationpath__", "/"),
                v,
                methods=[getattr(v, "__invocationmethod__")],
                summary=v.__name__,
            )
    return router
