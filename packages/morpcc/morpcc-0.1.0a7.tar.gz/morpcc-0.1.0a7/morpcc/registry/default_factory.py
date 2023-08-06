class DefaultFactoryRegistry(object):
    def __init__(self):
        self.names = []

    def register(self, name):
        if name not in self.names:
            self.names.append(name)

    def get(self, name, request):
        try:
            factory = request.app.get_default_factory(name)
        except NotImplementedError:
            factory = None

        if factory is None:
            raise KeyError("No default factory registered for %s" % name)

        return factory

    def get_factories(self, request):
        res = {}
        for k in self.names:
            res[k] = self.get(k, request)
        return res
