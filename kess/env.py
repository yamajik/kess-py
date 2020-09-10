import os

PRODUCTION = bool(os.getenv("PRODUCTION"))
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
FUNCTIONS_FOLDER = os.getenv("FUNCTIONS_FOLDER", "./functions")
PREFIX = os.getenv("PREFIX", "")
