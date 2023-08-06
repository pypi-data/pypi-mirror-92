from ..app import App
from .model import PageModel, PageCollection
from .modelui import PageCollectionUI, PageModelUI
from morpfw.crud import permission as crudperm


@App.permission_rule(model=PageCollection, permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True


@App.permission_rule(model=PageModel, permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True


@App.permission_rule(model=PageCollectionUI, permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True


@App.permission_rule(model=PageModelUI, permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True
