import httpx


class InternalRPC:
    _runtime: str
    _fn: str
    _version: str

    def __init__(self, runtime=None, fn=None, version="v1"):
        self._runtime = runtime
        self._fn = fn
        self._version = version

    def runtime(self, name):
        self._runtime = name
        return self

    def rt(self, name):
        return self.runtime(name)

    def fn(self, name, version="v1"):
        self._fn = name
        self._version = version
        return self

    @property
    def base_url(self):
        return f"http://{self._runtime}"

    def url(self, path):
        return f"/{self._fn}/{self._version}{path}"

    async def call(self, **kwargs):
        method = kwargs.pop("method", "post")
        path = kwargs.pop("path", "")
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            resp = await getattr(client, method)(self.url(path), **kwargs)
            return resp.json()

    async def post(self, **kwargs):
        kwargs["method"] = "post"
        return await self.call(**kwargs)

    async def get(self, **kwargs):
        kwargs["method"] = "get"
        return await self.call(**kwargs)

    async def __call__(self, **kwargs):
        return await self.post(**kwargs)


internal = InternalRPC()
runtime = internal.runtime
rt = internal.rt
fn = internal.fn
