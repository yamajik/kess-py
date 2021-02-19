import os
from collections import defaultdict
from typing import DefaultDict, Dict, Generator

from fastapi import FastAPI

from kess import env, imports
from kess.function import Function


class App(FastAPI):
    production: bool
    functions_folder: str
    runtime_prefix: str
    runtime_name: str
    functions: DefaultDict[str, Dict[str, Function]]

    def __init__(self, *args, **kwargs):
        self.functions_folder = kwargs.pop("functions_folder", env.FN_FOLDER)
        self.runtime_prefix = kwargs.pop("runtime_prefix", env.RUNTIME_PREFIX)
        self.runtime_name = kwargs.pop("runtime_name", env.RUNTIME_NAME)
        self.functions = defaultdict(dict)
        super().__init__(*args, **kwargs)

    @property
    def route_prefix(self):
        return f"{self.runtime_prefix}"

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
                        module = imports.import_module(os.path.splitext(function_file_path)[0].replace(os.path.sep, "."))
                        yield function_name, function_version, module.fn

    def scan_dev_functions(
        self, functions_folder: str
    ) -> Generator[(str, str, Function)]:
        for function_file_name in os.listdir(functions_folder):
            function_file_path = os.path.join(functions_folder, function_file_name)
            if os.path.isfile(function_file_path):
                function_name = os.path.splitext(function_file_name)[0]
                function_version = "latest"
                module = imports.import_module(os.path.splitext(function_file_path)[0].replace(os.path.sep, "."))
                yield function_name, function_version, module.fn

    def scan_functions(
        self, functions_folder: str, production: bool = False
    ) -> Generator[(str, str, Function)]:
        scanner = self.scan_prod_functions if production else self.scan_dev_functions
        yield from scanner(functions_folder)

    def setup_function(self, fn: Function, name: str, version: str, prefix: str = ""):
        fn.state.app = self
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
            self.functions_folder, production=True, prefix=self.route_prefix
        )
