from kess import Actor, actormethod

class ExecV2(Actor):
    @actormethod("test")
    async def test(self, data: object) -> object:
        return {"test": "data", **data}

    async def testv(self, data: object) -> object:
        return {"testv": "data", **data}
