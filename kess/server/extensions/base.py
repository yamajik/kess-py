import fastapi


class Extension:
    app: fastapi.FastAPI

    def __init__(self, app: fastapi.FastAPI):
        self.app = app

    def setup(self):
        ...
