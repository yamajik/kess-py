import os
from collections import defaultdict
from typing import DefaultDict, Dict, Generator

from fastapi import FastAPI

from kess import env, imports
from kess.function import Function


class App(FastAPI):
    production: bool
    functions_folder: str
    route_prefix: str
    functions: DefaultDict[str, Dict[str, Function]]

    def __init__(self, *args, **kwargs):
        self.production = kwargs.pop("production", env.PRODUCTION)
        self.functions_folder = kwargs.pop("functions_folder", env.FUNCTIONS_FOLDER)
        self.route_prefix = kwargs.pop("router_prefix", env.ROUTER_PREFIX)
        self.functions = defaultdict(dict)
        super().__init__(*args, **kwargs)

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

    def setup_function(self, fn: Function, name: str, version: str, prefix: str = ""):
        self.mount(f"{prefix}/{name}/{version}", fn)
        self.functions[name][version] = fn

    def setup_functions(
        self, functions_folder: str, production: bool = False, prefix: str = ""
    ):
        for name, version, fn in self.scan_functions(
            functions_folder, production=production
        ):
            self.setup_function(fn, name, version, prefix=prefix)

    def setup(self):
        super().setup()
        self.setup_functions(
            self.functions_folder, production=self.production, prefix=self.route_prefix
        )
