from ..app import App
from .model import NotificationCollection, NotificationModel

#
from .modelui import NotificationCollectionUI, NotificationModelUI
from .path import get_collection, get_model
from .schema import NotificationSchema

#


@App.typeinfo(name="morpcc.notification", schema=NotificationSchema)
def get_typeinfo(request):
    return {
        "title": "Notification",
        "description": "Notification type",
        "schema": NotificationSchema,
        "collection": NotificationCollection,
        "collection_factory": get_collection,
        "model": NotificationModel,
        "model_factory": get_model,
        "internal": True,
        #
        "collection_ui": NotificationCollectionUI,
        "model_ui": NotificationModelUI,
        #
    }
