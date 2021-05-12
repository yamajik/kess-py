from typing import Dict

import fastapi
from kess import env
from kess.server import extensions
from pydantic.main import BaseModel


class AppOptions(BaseModel):
    functions_folder: str = env.FN_FOLDER
    runtime_prefix: str = env.RUNTIME_PREFIX
    runtime_name: str = env.RUNTIME_NAME


class App(fastapi.FastAPI):
    options: AppOptions
    extensions: Dict[str, exceptions.Extension]

    def __init__(self, *args, **kwargs):
        self.options = kwargs.pop("options", AppOptions())
        self.extensions = {
            "modules": extensions.Modules(
                self, extensions.ModulesOptions(path=self.options.functions_folder)
            )
        }
        super().__init__(*args, **kwargs)
        self.on_event("startup")(self.on_start_up)

    def on_start_up(self):
        for ext in self.extensions.values():
            ext.setup()
