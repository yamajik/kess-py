from typing import Callable, Union

from kess import actor, invocation


class Function(actor.Actor, invocation.Invocation):
    ...


class FunctionMethod:
    actormethod: actor.ActorMethod
    invocationmethod: invocation.InvocationMethod

    def __init__(
        self,
        actormethod: actor.ActorMethod,
        invocationmethod: invocation.InvocationMethod,
    ):
        self.actormethod = actormethod
        self.invocationmethod = invocationmethod

    def __call__(self, func_or_name: Union[Callable, str]):
        return self.m(func_or_name)

    def wrap(self, func: Callable, name: str):
        self.actormethod.wrap(func, name)
        self.invocationmethod.wrap(func, path=f"/{name}")
        return func

    def m(self, func_or_name: Union[Callable, str]):
        if callable(func_or_name):
            return self.wrap(func_or_name, func_or_name.__name__)

        def wrapper(funcobj):
            return self.wrap(funcobj, func_or_name)

        return wrapper

    @property
    def actor(self):
        return self.actormethod

    @property
    def invocation(self):
        return self.invocationmethod


m = method = FunctionMethod(actor.method, invocation.method)

create_actor = actor.create
create_router = invocation.create
create_proxy = actor.create_proxy
invoke = actor.invoke
