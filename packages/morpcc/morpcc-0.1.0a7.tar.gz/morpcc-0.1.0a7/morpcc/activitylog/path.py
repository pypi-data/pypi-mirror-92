from ..app import App
from .model import ActivityLogModel, ActivityLogCollection
# 
from .modelui import ActivityLogModelUI, ActivityLogCollectionUI
# 
from .storage import ActivityLogStorage


def get_collection(request):
    storage = ActivityLogStorage(request)
    return ActivityLogCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=ActivityLogCollection,
          path='/api/v1/activitylog')
def _get_collection(request):
    return get_collection(request)


@App.path(model=ActivityLogModel,
          path='/api/v1/activitylog/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


@App.path(model=ActivityLogCollectionUI,
          path='/activitylog')
def _get_collection_ui(request):
    collection = get_collection(request)
    return collection.ui()


@App.path(model=ActivityLogModelUI,
          path='/activitylog/{identifier}')
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

# 
