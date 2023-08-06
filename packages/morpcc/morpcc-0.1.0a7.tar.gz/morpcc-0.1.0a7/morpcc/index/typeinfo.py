from ..app import App
from .model import IndexCollection, IndexModel

#
from .modelui import IndexCollectionUI, IndexModelUI
from .path import get_collection, get_model
from .schema import IndexSchema

#


@App.typeinfo(name="morpcc.index", schema=IndexSchema)
def get_typeinfo(request):
    return {
        "title": "Index",
        "description": "Index type",
        "schema": IndexSchema,
        "collection": IndexCollection,
        "collection_factory": get_collection,
        "model": IndexModel,
        "model_factory": get_model,
        #
        "collection_ui": IndexCollectionUI,
        "model_ui": IndexModelUI,
        "internal": True
        #
    }
