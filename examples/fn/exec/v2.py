from kess import Actor, actormethod, ActorProxy, actorinvoke


class ExecV2(Actor):
    @actormethod("apiv1")
    async def apiv1(self, data: object) -> object:
        return {"data": "apiv1", **await ActorProxy(ExecV2).apiv3(data)}

    @actormethod("apiv2")
    async def apiv2(self, data: object) -> object:
        return {"data": "apiv2", **await ActorProxy(name="ExecV2").invoke("apiv3", data=data)}

    @actormethod("apiv3")
    async def apiv3(self, data: object) -> object:
        return {"data": "apiv3", **data}

    async def notapi(self, data: object) -> object:
        return {"data": "notapi", **data}
