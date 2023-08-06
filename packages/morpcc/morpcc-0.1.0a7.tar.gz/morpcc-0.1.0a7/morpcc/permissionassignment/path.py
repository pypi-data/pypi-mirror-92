from ..app import App
from .model import PermissionAssignmentModel, PermissionAssignmentCollection
# 
from .modelui import PermissionAssignmentModelUI, PermissionAssignmentCollectionUI
# 
from .storage import PermissionAssignmentStorage


def get_collection(request):
    storage = PermissionAssignmentStorage(request)
    return PermissionAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=PermissionAssignmentCollection,
          path='/api/v1/permissionassignment')
def _get_collection(request):
    return get_collection(request)


@App.path(model=PermissionAssignmentModel,
          path='/api/v1/permissionassignment/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


@App.path(model=PermissionAssignmentCollectionUI,
          path='/permissionassignment')
def _get_collection_ui(request):
    collection = get_collection(request)
    return collection.ui()


@App.path(model=PermissionAssignmentModelUI,
          path='/permissionassignment/{identifier}')
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

# 
