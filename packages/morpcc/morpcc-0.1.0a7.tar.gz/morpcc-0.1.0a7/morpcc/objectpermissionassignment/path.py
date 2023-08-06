from ..app import App
from .model import ObjectPermissionAssignmentModel, ObjectPermissionAssignmentCollection
# 
from .modelui import ObjectPermissionAssignmentModelUI, ObjectPermissionAssignmentCollectionUI
# 
from .storage import ObjectPermissionAssignmentStorage


def get_collection(request):
    storage = ObjectPermissionAssignmentStorage(request)
    return ObjectPermissionAssignmentCollection(request, storage)


def get_model(request, identifier):
    col = get_collection(request)
    return col.get(identifier)


@App.path(model=ObjectPermissionAssignmentCollection,
          path='/api/v1/objectpermissionassignment')
def _get_collection(request):
    return get_collection(request)


@App.path(model=ObjectPermissionAssignmentModel,
          path='/api/v1/objectpermissionassignment/{identifier}')
def _get_model(request, identifier):
    return get_model(request, identifier)

# 


@App.path(model=ObjectPermissionAssignmentCollectionUI,
          path='/objectpermissionassignment')
def _get_collection_ui(request):
    collection = get_collection(request)
    return collection.ui()


@App.path(model=ObjectPermissionAssignmentModelUI,
          path='/objectpermissionassignment/{identifier}')
def _get_model_ui(request, identifier):
    model = get_model(request, identifier)
    if model:
        return model.ui()

# 
