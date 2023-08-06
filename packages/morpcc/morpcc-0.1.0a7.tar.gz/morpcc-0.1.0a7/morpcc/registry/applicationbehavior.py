class ApplicationBehaviorRegistry(object):
    def __init__(self):
        self.behaviors = []

    def register_behavior(self, name):
        if name not in self.behaviors:
            self.behaviors.append(name)

    def get_behavior(self, name, request):
        try:
            factory = request.app.get_application_behavior_factory(name)
        except NotImplementedError:
            factory = None

        if factory is None:
            raise KeyError("No behavior registered for %s" % name)

        result = factory(request)
        result.__name__ = name
        return result

    def get_behaviors(self, request):
        res = {}
        for k in self.behaviors:
            res[k] = self.get_behavior(k, request)
        return res
