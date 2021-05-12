from types import List

import dapr.actor
import fastapi
from dapr.ext.fastapi import DaprActor
from kess.server.extensions import base
from pydantic import BaseModel


class ActorOptions(BaseModel):
    ...


class Actor(base.Extension):
    options: ActorOptions
    actor: DaprActor
    actors: List[dapr.actor.Actor]

    def __init__(self, app: fastapi.FastAPI, options: ActorOptions):
        super().__init__(app)
        self.options = options
        self.actor = DaprActor(app)
        self.actors = []

    def push(self, *actors: List[dapr.actor.Actor]):
        self.actors.extend(actors)

    def setup(self):
        for actor in self.actors:
            self.actor.register_actor(actor)
