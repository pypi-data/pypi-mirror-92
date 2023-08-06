import rulez


class ReferenceValidator(object):
    def __init__(self, resource_type, attribute="uuid"):
        self.resource_type = resource_type
        self.attribute = attribute

    def __call__(self, request, schema, field, value, mode=None):
        resource = self.get_resource(request, value)
        if not resource:
            return "Invalid reference : {}".format(value)

    def get_resource(self, request, identifier):
        typeinfo = request.app.config.type_registry.get_typeinfo(
            name=self.resource_type, request=request
        )
        if not (identifier or "").strip():
            return None
        col = typeinfo["collection_factory"](request)
        models = col.search(rulez.field[self.attribute] == identifier)
        if models:
            return models[0]
        return None
