from kess import Actor, ActorProxy, actormethod,


class ExecV2(Actor):
    @actormethod
    async def apiv1(self, data: object) -> object:
        return {"data": "apiv1", **await ActorProxy(ExecV2).apiv4(data)}

    @actormethod("apiv2")
    async def apiv2(self, data: object) -> object:
        return {"data": "apiv2", **await ActorProxy(name="ExecV2").invoke("apiv4", data=data)}

    @actormethod("apiv4")
    async def apiv3(self, data: object) -> object:
        return {"data": "apiv3", **data}

    async def notapi(self, data: object) -> object:
        return {"data": "notapi", **data}
