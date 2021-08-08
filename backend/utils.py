def after(method_name):
    def _after(func):
        def __after(self, *args, **kwargs):
            rt = func(self, *args, **kwargs)
            getattr(self, method_name)()
            return rt
        return __after
    return _after


async def await_after(method_name):
    async def _await_after(func):
        async def __await_after(self, *args, **kwargs):
            func(self, *args, **kwargs)
            await getattr(self, method_name)()
        return __await_after
    return _await_after
