from ..app import App
from .model import ProcessCollection, ProcessModel

#
from .modelui import ProcessCollectionUI, ProcessModelUI

#
from .storage import ProcessStorage


def get_collection(request):
    blobstorage = request.app.get_config_blobstorage(request)
    storage = ProcessStorage(request, blobstorage=blobstorage)
    return ProcessCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=ProcessCollection, path="/api/v1/process")
def _get_collection(request):
    return get_collection(request)


@App.path(model=ProcessModel, path="/api/v1/process/{identifier}")
def _get_model(request, identifier):
    return get_model(request, identifier)


#


@App.path(model=ProcessCollectionUI, path="/process")
def _get_collection_ui(request):
    collection = get_collection(request)
    return collection.ui()


@App.path(model=ProcessModelUI, path="/process/{identifier}")
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()


#
