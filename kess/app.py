import glob
import inspect
import os
from types import ModuleType
from typing import Iterator, List

from dapr.actor import Actor
from dapr.ext.fastapi import DaprActor
from fastapi import APIRouter, FastAPI

from kess import actor, env, imports, invocation


class App(FastAPI):
    production: bool
    functions_folder: str
    runtime_prefix: str
    runtime_name: str
    routers: List[APIRouter]
    actors: List[Actor]

    def __init__(self, *args, **kwargs):
        self.functions_folder = kwargs.pop("functions_folder", env.FN_FOLDER)
        self.runtime_prefix = kwargs.pop("runtime_prefix", env.RUNTIME_PREFIX)
        self.runtime_name = kwargs.pop("runtime_name", env.RUNTIME_NAME)
        self.routers = []
        self.actors = []
        super().__init__(*args, **kwargs)

        actor = DaprActor(self)

        @self.on_event("startup")
        async def _startup():
            for r in self.routers:
                self.include_router(r)
            for a in self.actors:
                await actor.register_actor(a)

    @property
    def route_prefix(self):
        return f"{self.runtime_prefix}"

    def scan_functions(self, functions_folder: str) -> Iterator[ModuleType]:
        for file_path in glob.iglob(os.path.join(functions_folder, "**", "*.py")):
            yield imports.import_module(
                os.path.splitext(file_path)[0].replace(os.path.sep, ".")
            )

    def setup_function(self, module: ModuleType):
        for k, v in module.__dict__.items():
            if k.startswith("_") or not inspect.isclass(v):
                continue
            if v is not invocation.Invocation and issubclass(v, invocation.Invocation):
                self.routers.append(invocation.create(v))
            elif v is not actor.Actor and issubclass(v, actor.Actor):
                self.actors.append(actor.create(v))

    def setup_functions(self, functions_folder: str):
        for module in self.scan_functions(functions_folder):
            self.setup_function(module)

    def setup(self):
        super().setup()
        self.setup_functions(self.functions_folder)
