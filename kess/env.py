import os

PRODUCTION = bool(os.getenv("KESS_PRODUCTION"))
HOST = os.getenv("KESS_HOST", "0.0.0.0")
PORT = int(os.getenv("KESS_PORT", "8000"))
FUNCTIONS_FOLDER = os.getenv("KESS_FUNCTIONS_FOLDER", "functions")
ROUTER_PREFIX = os.getenv("KESS_ROUTE_PREFIX", "")
