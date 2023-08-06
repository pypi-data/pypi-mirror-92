from ..app import App
from .model import ActivityLogCollection, ActivityLogModel

#
from .modelui import ActivityLogCollectionUI, ActivityLogModelUI
from .path import get_collection, get_model
from .schema import ActivityLogSchema

#


@App.typeinfo(name="morpcc.activitylog", schema=ActivityLogSchema)
def get_typeinfo(request):
    return {
        "title": "ActivityLog",
        "description": "ActivityLog type",
        "schema": ActivityLogSchema,
        "collection": ActivityLogCollection,
        "collection_factory": get_collection,
        "model": ActivityLogModel,
        "model_factory": get_model,
        #
        "collection_ui": ActivityLogCollectionUI,
        "model_ui": ActivityLogModelUI,
        "internal": True
        #
    }
