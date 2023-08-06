from ..app import App
from .model import PageCollection, PageModel
from .modelui import PageCollectionUI, PageModelUI
from .path import get_collection, get_model
from .schema import PageSchema


@App.typeinfo(name="democms.page", schema=PageSchema)
def get_typeinfo(request):
    return {
        "title": "Page",
        "description": "A simple page content type",
        "collection": PageCollection,
        "collection_factory": get_collection,
        "collection_ui": PageCollectionUI,
        "model": PageModel,
        "model_factory": get_model,
        "model_ui": PageModelUI,
        "schema": PageSchema,
        "icon": 'file'
    }
