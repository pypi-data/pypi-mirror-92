import rulez
from colander import Invalid, null
from deform.compat import string_types
from deform.widget import SelectWidget, Widget
from morpfw.authn.pas.user.path import get_user_collection

from ..users.model import UserModelUI
from ..users.path import get_user_collection_ui


class ReferenceWidget(SelectWidget):
    template = "reference"
    readonly_template = "readonly/reference"
    null_value = ""
    values = ()
    multiple = False

    def __init__(
        self,
        resource_type,
        term_field="title",
        value_field="uuid",
        get_search_url=None,
        **kwargs
    ):
        self.resource_type = resource_type
        self.term_field = term_field
        self.value_field = value_field
        self.get_search_url = get_search_url
        if kwargs.get("placeholder", None) is None:
            kwargs["placeholder"] = " "
        super().__init__(**kwargs)

    def deserialize(self, *args, **kwargs):
        result = super().deserialize(*args, **kwargs)
        return result

    def get_resource_search_url(self, context, request):
        if self.get_search_url is None:
            baselink = request.relative_url("/+term-search")
        else:
            baselink = self.get_search_url(self, context, request)
        if "?" not in baselink:
            baselink += "?"
        else:
            baselink += "&"
        return baselink + "resource_type=%s&term_field=%s&value_field=%s" % (
            self.resource_type,
            self.term_field,
            self.value_field,
        )

    def get_resource_url(self, request, identifier):
        m = self.get_resource(request, identifier)
        if not m:
            return None
        return request.link(m)

    def get_resource(self, request, identifier):
        if not (identifier or "").strip():
            return None

        col = request.get_collection(self.resource_type)
        if not getattr(col, "ui", None):
            typeinfo = request.app.config.type_registry.get_typeinfo(
                name=self.resource_type, request=request
            )
            col = typeinfo["collection_ui_factory"](request)
        else:
            col = col.ui()
        models = col.search(rulez.field[self.value_field] == identifier)
        if models:
            return models[0]
        return None

    def get_resource_term(self, request, identifier):
        m = self.get_resource(request, identifier)
        if not m:
            return None
        return m.model[self.term_field]


class UserReferenceWidget(ReferenceWidget):
    def __init__(
        self,
        resource_type="morpfw.pas.user",
        term_field="username",
        value_field="uuid",
        **kwargs
    ):
        super().__init__(resource_type, term_field, value_field, **kwargs)

    def get_resource(self, request, identifier):
        if not identifier:
            return None
        users = get_user_collection(request)
        user = users.get_by_uuid(identifier)
        if user:
            return UserModelUI(request, user, get_user_collection_ui(request))
        return None
