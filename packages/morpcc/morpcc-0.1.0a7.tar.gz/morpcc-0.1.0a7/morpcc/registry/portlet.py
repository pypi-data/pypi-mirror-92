from morepath.toposort import Info, toposorted

from ..util import permits


class PortletRegistry(object):
    def __init__(self):
        self._portlets = {}
        self._portlet_options = {}

    def register(self, portlet_factory, name, template, permission):
        self._portlets[name] = {
            "factory": portlet_factory,
            "template": template,
            "name": name,
            "permission": permission,
        }

    def get_portlet(self, name):
        info = self._portlets[name]
        return Portlet(**info)


class PortletProviderRegistry(object):
    def __init__(self):
        self._providers = {}

    def register(self, provider_factory, name, permission):
        self._providers[name] = {
            "factory": provider_factory,
            "permission": permission,
            "name": name,
        }

    def get_provider(self, name):
        if name not in self._providers:
            return None

        info = self._providers[name]
        return PortletProvider(**info)


class Portlet(object):
    def __init__(self, name, factory, template, permission):
        self.name = name
        self.factory = factory
        self.template = template
        self.permission = permission

    def render(self, context, request, load_template):
        portletdata = self.factory(context, request)

        def _permits(permission, request=request, context=context):
            return permits(request, context, permission)

        if self.permission and not permits(request, context, self.permission):
            return ""

        if self.template is None:
            assert isinstance(portletdata, str)
            return portletdata
        else:
            template = load_template(self.template)
            data = {
                "permits": _permits,
                "app": request.app,
                "settings": request.app.settings,
                "request": request,
                "context": context,
                "load_template": load_template,
            }
            data.update(portletdata)
            return template.render(**data)


class PortletProvider(object):
    def __init__(self, factory, permission, name):
        self.name = name
        self.factory = factory
        self.permission = permission

    def render(self, context, request, load_template):

        if self.permission and not permits(request, context, self.permission):
            return ""

        portletnames = self.factory(context, request)

        portlets = []
        for pname in portletnames:
            portlet = request.app.config.portlet_registry.get_portlet(pname)
            portlets.append(portlet)

        result = []

        for portlet in portlets:
            result.append(portlet.render(context, request, load_template))

        return "\n".join(result)
