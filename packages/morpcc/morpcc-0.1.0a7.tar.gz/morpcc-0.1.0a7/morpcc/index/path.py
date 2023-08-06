from ..app import App
from .model import IndexCollection, IndexModel

#
from .modelui import IndexCollectionUI, IndexModelUI

#
from .storage import IndexStorage


def get_collection(request):
    storage = IndexStorage(request)
    return IndexCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=IndexCollection, path="/api/v1/index")
def _get_collection(request):
    return get_collection(request)


@App.path(model=IndexModel, path="/api/v1/index/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


#


@App.path(model=IndexCollectionUI, path="/index")
def _get_collection_ui(request):
    collection = get_collection(request)
    if collection:
        return collection.ui()


@App.path(model=IndexModelUI, path="/index/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

#

