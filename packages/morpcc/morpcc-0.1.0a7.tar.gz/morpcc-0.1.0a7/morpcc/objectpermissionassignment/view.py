import rulez
from morpcc.crud.model import ModelUI
from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw.crud import permission as crudperm

from ..app import App
from ..permission import ManagePermission
from .model import ObjectPermissionAssignmentCollection, ObjectPermissionAssignmentModel

#
from .modelui import (
    ObjectPermissionAssignmentCollectionUI,
    ObjectPermissionAssignmentModelUI,
)

#


@App.html(
    model=ModelUI,
    name="manage-permissions",
    template="master/permission/model.pt",
    permission=ManagePermission,
)
def manage_permission(context, request):
    return {"page_title": "Manage Permissions"}
