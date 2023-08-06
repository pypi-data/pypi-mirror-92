import os

from morpfw.authn.pas.user.model import UserModel
from morpfw.crud.blobstorage.fsblobstorage import FSBlobStorage

from ..app import App
from ..crud.model import CollectionUI, ModelUI


@App.blobstorage(model=UserModel)
def get_user_blobstorage(model, request):
    return request.app.get_config_blobstorage(request)


class UserModelUI(ModelUI):

    view_exclude_fields = ModelUI.view_exclude_fields + ["password", "nonce"]
    edit_include_fields = ["email", "timezone"]


class UserCollectionUI(CollectionUI):

    modelui_class = UserModelUI

    page_title = "Users"
    listing_title = "Registered Users"
    create_view_enabled = True

    columns = [
        {"title": "Username", "name": "username"},
        {"title": "Created", "name": "created"},
        {"title": "State", "name": "state"},
        {"title": "Source", "name": "source"},
        {"title": "Actions", "name": "structure:buttons"},
    ]


class CurrentUserModelUI(UserModelUI):
    pass
