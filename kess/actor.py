import abc
from typing import Type

from dapr import actor

Remindable = actor.Remindable


class Actor(abc.ABC):
    pass


def method(name: str = None):
    def wrapper(funcobj):
        funcobj.__actormethod__ = name
        return funcobj

    return wrapper


def create(name: str, obj: Type[Actor]) -> Type[actor.Actor]:
    injects = {
        k: v
        for k, v in obj.__dict__.items()
        if not k.startswith("_") and callable(v) and hasattr(v, "__actormethod__")
    }
    Interface = type(name, (actor.ActorInterface,), injects)
    return type(name, (actor.Actor, Interface), {})
