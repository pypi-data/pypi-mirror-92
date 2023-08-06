from ..app import App
from .model import SettingCollection, SettingModel

#
from .modelui import SettingCollectionUI, SettingModelUI

#
from .storage import SettingStorage


def get_collection(request):
    storage = SettingStorage(request)
    return SettingCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=SettingCollection, path="/api/v1/setting")
def _get_collection(request):
    return get_collection(request)


@App.path(model=SettingModel, path="/api/v1/setting/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=SettingCollectionUI, path="/site-settings/setting")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=SettingModelUI, path="/site-settings/setting/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

#

