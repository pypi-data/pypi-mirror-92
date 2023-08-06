class DataSource(object):
    def __init__(self, name, factory, request, cache_config=None):
        self.factory = factory
        self.request = request
        self.name = name
        self.cache_config = cache_config or {}

    def get_cache(self):
        cache_key = "morpcc.datasource.%s" % self.name
        cache = self.request.cache.get_cache(cache_key, **self.cache_config)
        return cache

    def compute(self):
        name = self.name
        request = self.request
        factory = self.factory

        cache = self.get_cache()

        def create():
            return factory(request)

        return cache.get(key=name, createfunc=create)

    def clear_cache(self):
        cache = self.get_cache()
        cache.clear()


class DataSourceRegistry(object):
    default_cache_config = {
        "expire": 10,
    }

    def __init__(self):
        self.names = []
        self.cache_config = {}

    def register(self, name, **kwargs):
        if name not in self.names:
            self.names.append(name)

        for k, v in self.default_cache_config.items():
            if k not in kwargs:
                kwargs[k] = v

        if name not in self.cache_config:
            self.cache_config[name] = kwargs
        else:
            for k, v in kwargs.items():
                self.cache_config[name][k] = v

    def get(self, name, request):
        factory = self.get_factory(name, request)
        return DataSource(name, factory, request, self.cache_config[name])

    def get_factory(self, name, request):
        try:
            factory = request.app.get_datasource_factory(name)
        except NotImplementedError:
            factory = None

        if factory is None:
            raise KeyError("No default factory registered for %s" % name)

        return factory

    def get_factories(self, request):
        res = {}
        for k in self.names:
            res[k] = self.get_factory(k, request)
        return res
