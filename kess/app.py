import logging
import os
from typing import Dict, Generator

import uvicorn
from fastapi import FastAPI

from . import env, imports
from .function import Function


class App:
    app: FastAPI
    functions: Dict[str, Function]
    logger: logging.Logger

    def __init__(self):
        self.app = FastAPI()
        self.functions = {}
        self.logger = logging.getLogger("fastapi")

    def scan_prod_functions(
        self, functions_folder: str
    ) -> Generator[(str, str, Function)]:
        for function_name in os.listdir(functions_folder):
            function_path = os.path.join(functions_folder, function_name)
            if os.path.isdir(function_path):
                for function_file_name in os.listdir(function_path):
                    function_file_path = os.path.join(function_path, function_file_name)
                    if os.path.isfile(function_file_path):
                        function_version = os.path.splitext(function_file_name)[0]
                        module = imports.import_file(function_file_path)
                        yield function_name, function_version, module.fn

    def scan_dev_functions(
        self, functions_folder: str
    ) -> Generator[(str, str, Function)]:
        for function_file_name in os.listdir(functions_folder):
            function_file_path = os.path.join(functions_folder, function_file_name)
            if os.path.isfile(function_file_path):
                function_name = os.path.splitext(function_file_name)[0]
                module = imports.import_file(function_file_path)
                yield function_name, "latest", module.fn

    def scan_functions(
        self, functions_folder: str, production: bool = False
    ) -> Generator[(str, str, Function)]:
        scanner = self.scan_prod_functions if production else self.scan_dev_functions
        yield from scanner(functions_folder)

    def setup_function(self, fn: Function, name: str, version: str):
        fn.setup(name, version)
        self.app.mount(fn.prefix(), fn.app)
        self.functions[name] = fn

    def setup(self, **kwargs):
        production = kwargs.get("production", env.PRODUCTION)
        functions_folder = kwargs.get("functions_folder", env.FUNCTIONS_FOLDER)
        for name, version, fn in self.scan_functions(
            functions_folder, production=production
        ):
            self.setup_function(fn, name, version)

    def run(self, **kwargs):
        kwargs.pop("reload", None)
        uvicorn.run(self.app, **kwargs)
