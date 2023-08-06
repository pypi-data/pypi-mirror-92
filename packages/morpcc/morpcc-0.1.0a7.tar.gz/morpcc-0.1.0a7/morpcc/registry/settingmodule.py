from morepath.toposort import Info, toposorted


class SettingModuleRegistry(object):
    def __init__(self):
        self._setting_modules = {}
        self._infos = []

    def register(self, factory, name, title, under=None, over=None):
        self._infos.append(Info(name, over, under))
        self._setting_modules[name] = {"factory": factory, "name": name, "title": title}

    def _get(self, request, name):
        info = self._setting_modules[name]
        return {
            "name": info["name"],
            "title": info["title"],
            "modules": info["factory"](request) or [],
        }

    def _keys(self):
        """Sort key topologically by over and under.

        :return: a sorted list of infos.
        """
        return [info.key for info in toposorted(self._infos)]

    def modules(self, request):
        modules = []
        for k in self._keys():
            modules.append(self._get(request, k))

        return modules
