def after(method_name):
    def _after(func):
        def __after(self, *args, **kwargs):
            func(self, *args, **kwargs)
            getattr(self, method_name)()
        return __after
    return _after
