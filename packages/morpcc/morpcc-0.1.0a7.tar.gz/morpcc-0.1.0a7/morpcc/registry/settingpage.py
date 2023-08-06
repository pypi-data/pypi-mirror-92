import dataclasses

import colander
import deform
import morepath
from inverter import dc2colander, dc2colanderjson
from morepath.toposort import Info, toposorted
from morpfw.crud.errors import AlreadyExistsError, ValidationError
from morpfw.exc import ConfigurationError

from ..util import permits


class SettingPageRegistry(object):
    def __init__(self):
        self._setting_pages = {}

    def register(self, factory, name, title, permission, order=0):
        self._setting_pages[name] = {
            "factory": factory,
            "title": title,
            "name": name,
            "permission": permission,
            "order": order,
        }

    def get(self, request, name):
        info = self._setting_pages[name]
        return SettingPage(**info)

    def keys(self):
        return [
            i["name"]
            for i in sorted(self._setting_pages.values(), key=lambda x: x["order"])
        ]

    def values(self, request):
        return [self.get(request, k) for k in self.keys()]

    def items(self, request):
        return [(k, self.get(request, k)) for k in self.keys()]


class SettingPage(object):
    def __init__(self, factory, name, title, permission, order=0):
        self.factory = factory
        self.name = name
        self.title = title
        self.permission = permission
        self.order = order

    def enabled(self, context, request):
        if self.factory(request):
            if self.permission:
                if request.permits(context, self.permission):
                    return True
            else:
                return True
        return False

    def formschema(self, context, request):
        schema = self.factory(request)
        formschema = dc2colander.convert(
            schema, request=request, default_tzinfo=request.timezone()
        )()
        formschema = formschema.bind(context=context, request=request)
        return formschema

    def jsonformschema(self, context, request):
        schema = self.factory(request)
        field_metadata = {}
        for fname, field in schema.__dataclass_fields__.items():
            field_factory = field.metadata.get(
                "morpcc.setting.colander_field_factory", None
            )
            if field_factory:
                field_metadata.setdefault(fname, {})
                field_metadata[fname]["colander.field_factory"] = field_factory
        formschema = dc2colanderjson.convert(
            schema,
            request=request,
            default_tzinfo=request.timezone(),
            field_metadata=field_metadata,
        )()
        formschema = formschema.bind(context=context, request=request)
        return formschema

    def form(self, context, request):
        return deform.Form(self.formschema(context, request), buttons=("Submit",))

    def form_data(self, context, request):
        settings = request.get_collection("morpcc.setting")
        schema = self.factory(request)
        jsonformschema = self.jsonformschema(context, request)
        data = {}
        for name, field in schema.__dataclass_fields__.items():
            setting_key = field.metadata["morpcc.setting.key"]
            setting = settings.get_by_key(setting_key)
            value = (setting["data"] or {}).get("value", None)
            form_field = jsonformschema[name]
            if value is None:
                if not isinstance(field.default, dataclasses._MISSING_TYPE):
                    value = field.default
                elif not isinstance(field.default_factory, dataclasses._MISSING_TYPE):
                    value = field.default_factory()
            else:
                try:
                    value = form_field.deserialize(value)
                except colander.Invalid:
                    value = None
            data[name] = value
        return data
        # get keys

    def process_form(self, context, request):
        settings = request.get_collection("morpcc.setting")
        failed = False
        controls = list(request.POST.items())
        form = self.form(context, request)
        jsonformschema = self.jsonformschema(context, request)
        data = self.form_data(context, request)
        schema = self.factory(request)
        keys = schema.__dataclass_fields__.keys()
        failed = False
        try:
            data = form.validate(controls)
        except deform.ValidationFailure as e:
            form = e
            failed = True

        if not failed:
            for k, v in data.items():
                if k in keys:
                    field = schema.__dataclass_fields__[k]
                    setting_key = field.metadata["morpcc.setting.key"]
                    setting = settings.get_by_key(setting_key)
                    form_field = jsonformschema[k]
                    if v is not None:
                        value = form_field.serialize(v)
                    else:
                        value = v
                    setting.update({"key": setting_key, "data": {"value": value}})

            return None

        return {"form": form, "form_data": data}
