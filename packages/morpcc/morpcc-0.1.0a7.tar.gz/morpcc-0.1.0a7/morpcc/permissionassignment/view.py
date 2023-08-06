import rulez
from morpcc.crud.model import CollectionUI, ModelUI
from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw.crud import permission as crudperm
from morpfw.crud.model import Collection, Model

from ..app import App
from ..permission import ManagePermission
from .model import PermissionAssignmentCollection, PermissionAssignmentModel

#
from .modelui import PermissionAssignmentCollectionUI, PermissionAssignmentModelUI
