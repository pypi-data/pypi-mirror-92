from ..app import App
from .model import ObjectPermissionAssignmentCollection, ObjectPermissionAssignmentModel

#
from .modelui import (
    ObjectPermissionAssignmentCollectionUI,
    ObjectPermissionAssignmentModelUI,
)
from .path import get_collection, get_model
from .schema import ObjectPermissionAssignmentSchema

#


@App.typeinfo(
    name="morpcc.objectpermissionassignment", schema=ObjectPermissionAssignmentSchema
)
def get_typeinfo(request):
    return {
        "title": "ObjectPermissionAssignment",
        "description": "ObjectPermissionAssignment type",
        "schema": ObjectPermissionAssignmentSchema,
        "collection": ObjectPermissionAssignmentCollection,
        "collection_factory": get_collection,
        "model": ObjectPermissionAssignmentModel,
        "model_factory": get_model,
        #
        "collection_ui": ObjectPermissionAssignmentCollectionUI,
        "model_ui": ObjectPermissionAssignmentModelUI,
        "internal": True
        #
    }
