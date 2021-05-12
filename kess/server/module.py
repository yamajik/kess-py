from typing import Callable, Dict, Optional, Union

from kess import actor, invocation
from pydantic.main import BaseModel


class Module:
    ...


ModuleFunction = Callable[[Optional[BaseModel]], Union[BaseModel, Dict, None]]


class ModuleMethod:
    def __call__(self, name: str = ""):
        return self.wrap(name)

    def wrap(self, name: str):
        def _wrapper(func: Module):
            actor.method(f"/{name}")(func)
            invocation.method(name)(func)
            return func

        return _wrapper


m = method = ModuleMethod()

create_actor = actor.create
create_router = invocation.create
create_proxy = actor.create_proxy
invoke = actor.invoke
