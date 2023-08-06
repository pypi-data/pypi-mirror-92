from morpfw import FSBlobStorage

from ..app import App
from .model import PageCollection, PageModel
from .modelui import PageCollectionUI, PageModelUI
from .storage import PageStorage


def get_collection(request):
    blobstorage = request.app.get_config_blobstorage(request)
    storage = PageStorage(request, blobstorage=blobstorage)
    return PageCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=PageCollection, path="/api/v1/page")
def _get_collection(request):
    return get_collection(request)


@App.path(model=PageModel, path="/api/v1/page/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


@App.path(model=PageCollectionUI, path="/page")
def _get_collection_ui(request):
    col = get_collection(request)
    return col.ui()


@App.path(model=PageModelUI, path="/page/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()
