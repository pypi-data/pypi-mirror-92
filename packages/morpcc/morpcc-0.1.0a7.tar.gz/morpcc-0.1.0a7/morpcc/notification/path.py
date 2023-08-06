from ..app import App
from .model import NotificationCollection, NotificationModel

#
from .modelui import NotificationCollectionUI, NotificationModelUI

#
from .storage import NotificationStorage


def get_collection(request):
    storage = NotificationStorage(request)
    return NotificationCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=NotificationCollection, path="/api/v1/notification")
def _get_collection(request):
    return get_collection(request)


@App.path(model=NotificationModel, path="/api/v1/notification/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


#


@App.path(model=NotificationCollectionUI, path="/notification")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=NotificationModelUI, path="/notification/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()


#
