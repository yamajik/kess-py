import glob
import inspect
import os
from types import ModuleType
from typing import Iterator

import fastapi
from kess import actor, env, function, imports, invocation
from kess.server.extensions import base
from pydantic import BaseModel


class ModulesOptions(BaseModel):
    path: str


class Modules(base.Extension):
    options: ModulesOptions

    def __init__(self, app: fastapi.FastAPI, options: ModulesOptions):
        super().__init__(app)
        self.options = options

    def setup(self):
        self.setup_modules(self.options.path)

    def scan_modules(self, modules_folder: str) -> Iterator[ModuleType]:
        for file_path in glob.iglob(os.path.join(modules_folder, "**", "*.py")):
            yield imports.import_module(
                os.path.splitext(file_path)[0].replace(os.path.sep, ".")
            )

    def setup_module(self, module: ModuleType):
        for k, v in module.__dict__.items():
            if k.startswith("_") or not inspect.isclass(v):
                continue
            if issubclass(v, invocation.Invocation) and v not in (
                invocation.Invocation,
                function.Function,
            ):
                self.routers.append(invocation.create(v))
            if issubclass(v, actor.Actor) and v not in (actor.Actor, function.Function):
                self.actors.append(actor.create(v))

    def setup_modules(self, modules_folder: str):
        for module in self.scan_modules(modules_folder):
            self.setup_module(module)
