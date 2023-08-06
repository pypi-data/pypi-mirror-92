from morpfw.crud import permission as crudperm
from ..app import App
from .model import ActivityLogModel, ActivityLogCollection
from .modelui import ActivityLogModelUI, ActivityLogCollectionUI


@App.permission_rule(model=ActivityLogCollection,
                     permission=crudperm.All)
def allow_collection_access(identity, model, permission):
    return True

@App.permission_rule(model=ActivityLogModel,
                     permission=crudperm.All)
def allow_model_access(identity, model, permission):
    return True

# 

@App.permission_rule(model=ActivityLogCollectionUI,
                     permission=crudperm.All)
def allow_collection_ui_access(identity, model, permission):
    return True

@App.permission_rule(model=ActivityLogModelUI,
                     permission=crudperm.All)
def allow_model_ui_access(identity, model, permission):
    return True

# 
