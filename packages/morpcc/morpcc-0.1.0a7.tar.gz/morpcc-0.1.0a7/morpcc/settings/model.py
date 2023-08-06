import dataclasses

import morpfw
import rulez

from .modelui import SettingCollectionUI, SettingModelUI
from .schema import SettingSchema

_marker = object()


class SettingModel(morpfw.Model):
    schema = SettingSchema

    def ui(self):
        return SettingModelUI(self.request, self, self.collection.ui())


class SettingCollection(morpfw.Collection):
    schema = SettingSchema

    def ui(self):
        return SettingCollectionUI(self.request, self)

    @morpfw.requestmemoize()
    def get_by_key(self, key):
        self.request.environ.setdefault("morpcc.cache.settings", {})
        cachemgr = self.request.environ["morpcc.cache.settings"]
        if key in cachemgr:
            return cachemgr[key]

        items = self.all()
        for item in items:
            cachemgr[item["key"]] = item

        if key in cachemgr:
            return cachemgr[key]

        result = self.create({"key": key, "data": {"value": None}})
        cachemgr[key] = result
        return result

    def resolve_raw(self, key, default=_marker):
        """ return raw serialized settings value """
        item = self.get_by_key(key)
        if default is not _marker:
            return item["data"].get("value", default)
        return item["data"].get("value")

    def resolve(self, key, default=_marker):
        """ return deserialized settings value """
        item = self.get_by_key(key)
        pages = self.request.app.config.setting_page_registry.values(self.request)
        for p in pages:
            schema = p.factory(self.request)
            for fname, field in schema.__dataclass_fields__.items():
                if field.metadata.get("morpcc.setting.key", None) == key:
                    fschema = p.jsonformschema(self, self.request)
                    serde = fschema[fname]
                    value = item["data"]["value"]
                    if value is None:
                        if not isinstance(field.default, dataclasses._MISSING_TYPE):
                            value = field.default
                        elif not isinstance(
                            field.default_factory, dataclasses._MISSING_TYPE
                        ):
                            value = field.default_factory()
                    else:
                        value = serde.deserialize(value)
                    return value
        if default is _marker:
            raise KeyError(key)
        return default

    def store(self, key, value):
        item = self.get_by_key(key)
        pages = self.request.app.config.setting_page_registry.values(self.request)
        for p in pages:
            schema = p.factory(self.request)
            for fname, field in schema.__dataclass_fields__.items():
                if field.metadata.get("morpcc.setting.key", None) == key:
                    fschema = p.jsonformschema(self, self.request)
                    serde = fschema[fname]
                    value = serde.serialize(value)
                    item.update({"data": {"value": value}})
                    return
        raise KeyError(key)
