import functools
import inspect
from typing import Any, Callable, Dict, Optional, Type, Union

from dapr import actor
from dapr.serializers.json import DefaultJSONSerializer
from fastapi.dependencies import utils as fastapiutils
from kess.server import module
from pydantic import utils as pydanticuilts
from pydantic.main import BaseModel

OPTIONS_KEY = "__actor_options__"

defaultJSONSerializer = DefaultJSONSerializer()

Remindable = actor.Remindable


class ActorMethod:
    def __call__(self, name: str = ""):
        return self.wrap(name)

    def wrap(self, name: str):
        def _wrapper(func: module.ModuleFunction):
            setattr(func, OPTIONS_KEY, {"name": name or func.__name__})
            return func

        return _wrapper

    def wrap_model(self, func):
        ModelClass = self.find_modal_class(func)

        @functools.wraps(func)
        def _wrapper(self, data):
            if ModelClass is not None:
                data = ModelClass(**data)
            result = func(self, data)
            if isinstance(result, BaseModel):
                result = result.dict()
            return result

        return _wrapper

    def find_modal_class(self, func) -> Union[Type[BaseModel], None]:
        for _, value in fastapiutils.get_typed_signature(func).parameters.items():
            if inspect.isclass(value.annotation) and issubclass(
                value.annotation, BaseModel
            ):
                return value.annotation
        return None


m = method = ActorMethod()


def create(obj: Type[module.Module], name: str = None) -> Type[actor.Actor]:
    return create_interface(obj, name)


def create_interface(
    obj: Type[module.Module], name: str = None
) -> Type[actor.ActorInterface]:
    return create_interface_from_dict(dict(obj.__dict__), name or obj.__name__)


def create_interface_from_dict(obj: Dict, name: str) -> Type[actor.ActorInterface]:
    def _set(v):
        setattr(obj, "__actormethod__", getattr(v, OPTIONS_KEY)["name"])
        return v

    injects = {
        k: _set(v)
        for k, v in obj.items()
        if not k.startswith("_") and callable(v) and hasattr(v, OPTIONS_KEY)
    }
    return type(name, (actor.ActorInterface,), injects)


class ActorProxyFactory(actor.ActorProxyFactory):
    def create(
        self,
        actor_type: str,
        actor_id: actor.ActorId,
        actor_interface: Type[actor.ActorInterface] = None,
    ) -> "ActorProxy":
        return ActorProxy(
            self._dapr_client,
            actor_type,
            actor_id,
            actor_interface,
            self._message_serializer,
        )


class ActorProxy(actor.ActorProxy):
    _default_proxy_factory = ActorProxyFactory()

    async def invoke(self, method: str, data: Any = None) -> Any:
        raw_data = self._message_serializer.serialize(data)
        resp = await self.invoke_method(method, raw_data)
        return self._message_serializer.deserialize(resp)


def create_proxy(
    obj: Type[module.Module], name: str = None, id: str = None
) -> ActorProxy:
    name = name or obj.__name__
    actor_id = actor.ActorId(id) if id else actor.ActorId.create_random_id()
    Interface = create_interface(obj, name, id=id)
    return ActorProxy.create(name, actor_id, Interface)


def create_proxy_from_dict(obj: Dict, name: str, id: str = None) -> ActorProxy:
    actor_id = actor.ActorId(id) if id else actor.ActorId.create_random_id()
    Interface = create_interface_from_dict(obj, name=name)
    return ActorProxy.create(name, actor_id, Interface)


def create_proxy_from_none(name: str, id: str = None) -> ActorProxy:
    actor_id = actor.ActorId(id) if id else actor.ActorId.create_random_id()
    return ActorProxy.create(name, actor_id)


async def invoke(actor: str, method: str, id: str = None, data: Any = None) -> Any:
    return await create_proxy(name=actor).invoke(method, data)
