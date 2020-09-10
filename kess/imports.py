import importlib
from types import ModuleType
import uuid

import_module = importlib.import_module
reload = importlib.reload


def import_file(file_path: str, module_name: str = None) -> ModuleType:
    module_name = module_name or uuid.uuid4().hex
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
