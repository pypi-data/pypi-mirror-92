from ..app import App
from .model import ProcessCollection, ProcessModel

#
from .modelui import ProcessCollectionUI, ProcessModelUI
from .path import get_collection, get_model
from .schema import ProcessSchema

#


@App.typeinfo(name="morpcc.process", schema=ProcessSchema)
def get_typeinfo(request):
    return {
        "title": "Process",
        "description": "Process type",
        "schema": ProcessSchema,
        "collection": ProcessCollection,
        "collection_factory": get_collection,
        "model": ProcessModel,
        "model_factory": get_model,
        #
        "collection_ui": ProcessCollectionUI,
        "model_ui": ProcessModelUI,
        "internal": True
        #
    }
