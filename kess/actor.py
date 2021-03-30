from typing import Any, Callable, Dict, Type, Union

from dapr import actor
from dapr.serializers.json import DefaultJSONSerializer

defaultJSONSerializer = DefaultJSONSerializer()

Remindable = actor.Remindable


class Actor:
    ...


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


class ActorMethod:
    def __call__(self, func_or_name: Union[Callable, str]):
        return self.m(func_or_name)

    def wrap(self, func: Callable, name: str):
        func.__actormethod__ = name
        return func

    def m(self, func_or_name: Union[Callable, str]):
        if callable(func_or_name):
            return self.wrap(func_or_name, func_or_name.__name__)

        def wrapper(funcobj):
            return self.wrap(funcobj, func_or_name)

        return wrapper


m = method = ActorMethod()


def create_interface(obj: Type[Actor], name: str = None) -> Type[actor.ActorInterface]:
    return create_interface_from_dict(dict(obj.__dict__), name or obj.__name__)


def create_interface_from_dict(obj: Dict, name: str) -> Type[actor.ActorInterface]:
    injects = {
        k: v
        for k, v in obj.items()
        if not k.startswith("_") and callable(v) and hasattr(v, "__actormethod__")
    }
    return type(name, (actor.ActorInterface,), injects)


def create(obj: Type[Actor], name: str = None) -> Type[actor.Actor]:
    return create_from_dict(dict(obj.__dict__), name or obj.__name__)


def create_from_dict(obj: Dict, name: str) -> Type[actor.Actor]:
    Interface = create_interface_from_dict(obj, name)
    return type(name, (actor.Actor, Interface), obj)


def create_proxy(
    obj: Type[Actor] = None, name: str = None, id: str = None
) -> ActorProxy:
    if obj:
        return create_proxy_from_dict(dict(obj.__dict__), name or obj.__name__, id=id)
    return create_proxy_from_none(name, id=id)


def create_proxy_from_dict(obj: Dict, name: str, id: str = None) -> ActorProxy:
    actor_id = actor.ActorId(id) if id else actor.ActorId.create_random_id()
    Interface = create_interface_from_dict(obj, name=name)
    return ActorProxy.create(name, actor_id, Interface)


def create_proxy_from_none(name: str, id: str = None) -> ActorProxy:
    actor_id = actor.ActorId(id) if id else actor.ActorId.create_random_id()
    return ActorProxy.create(name, actor_id)


async def invoke(actor: str, method: str, id: str = None, data: Any = None) -> Any:
    return await create_proxy(name=actor).invoke(method, data)
