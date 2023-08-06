from ..app import App
from .model import PermissionAssignmentCollection, PermissionAssignmentModel

#
from .modelui import PermissionAssignmentCollectionUI, PermissionAssignmentModelUI
from .path import get_collection, get_model
from .schema import PermissionAssignmentSchema

#


@App.typeinfo(name="morpcc.permissionassignment", schema=PermissionAssignmentSchema)
def get_typeinfo(request):
    return {
        "title": "PermissionAssignment",
        "description": "PermissionAssignment type",
        "schema": PermissionAssignmentSchema,
        "collection": PermissionAssignmentCollection,
        "collection_factory": get_collection,
        "model": PermissionAssignmentModel,
        "model_factory": get_model,
        #
        "collection_ui": PermissionAssignmentCollectionUI,
        "model_ui": PermissionAssignmentModelUI,
        "internal": True,
        #
    }
