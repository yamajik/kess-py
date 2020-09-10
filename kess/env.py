import functools
import os

PRODUCTION = bool(os.getenv("KESS_PRODUCTION"))
HOST = os.getenv("KESS_HOST", "127.0.0.1")
PORT = int(os.getenv("KESS_PORT", "8000"))
FUNCTIONS_FOLDER = os.getenv("KESS_FUNCTIONS_FOLDER", "./functions")
ROUTER_PREFIX = os.getenv("KESS_ROUTE_PREFIX", "")


environ = os.environ


def String(value):
    return str(value)


def Int(value):
    return int(value)


def Float(value):
    return float(value)


def Bool(value):
    return value in ("true", "True")


def get(key, default=None, required=False, type=String):
    if key not in environ:
        if required:
            raise Exception(f"No such env: {key}")
        return default
    value = environ[key]
    try:
        return type(value)
    except Exception:
        raise Exception(f"EnvTypeErr: ({key}) {value} except {_get_type_name(type)}")


get_str = functools.partial(get, type=String)
get_int = functools.partial(get, type=Int)
get_float = functools.partial(get, type=Float)
get_bool = functools.partial(get, type=Bool)


def update(*args, **kwargs):
    return environ.update(*args, **kwargs)


def _get_type_name(type):
    name = getattr(type, "name", None) or getattr(type, "__name__", None)
    if not name:
        raise Exception(f"Unknown env type: {type}")
    return name
