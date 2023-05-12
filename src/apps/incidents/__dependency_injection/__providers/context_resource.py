def async_resource_context_factory(some_class):
    class AsyncResource(some_class):
        async def init(self):
            yield await self.__aenter__()

        async def shutdown(self):
            await self.__aexit__(None, None, None)

    return AsyncResource
