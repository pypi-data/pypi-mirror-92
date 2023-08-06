from morepath.toposort import Info, toposorted


class PermissionResolverRegistry(object):
    """Registry for tweens.
    """

    def __init__(self):
        self._infos = []

    def register_factory(self, factory, over, under):
        self._infos.append(Info(factory, over, under))

    def sorted_factories(self):
        """Sort factories topologically by over and under.

        :return: a sorted list of infos.
        """
        return [info.key for info in toposorted(self._infos)]

    def resolve(self, request, model, permission, identity):
        for factory in self.sorted_factories():
            result = factory(model, request, permission, identity)
            if result is not None:
                return result
        return None
