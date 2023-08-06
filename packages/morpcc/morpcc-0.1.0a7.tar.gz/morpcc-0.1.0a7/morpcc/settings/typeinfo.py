from ..app import App
from .model import SettingCollection, SettingModel

#
from .modelui import SettingCollectionUI, SettingModelUI
from .path import get_collection, get_model
from .schema import SettingSchema

#


@App.typeinfo(name="morpcc.setting", schema=SettingSchema)
def get_typeinfo(request):
    return {
        "title": "Setting",
        "description": "Setting",
        "schema": SettingSchema,
        "collection": SettingCollection,
        "collection_factory": get_collection,
        "model": SettingModel,
        "model_factory": get_model,
        #
        "collection_ui": SettingCollectionUI,
        "model_ui": SettingModelUI,
        "internal": True
        #
    }
