from morpfw.authn.pas.user.path import get_user, get_user_collection

from ..app import App
from .model import CurrentUserModelUI, UserCollectionUI, UserModelUI


@App.path(model=UserCollectionUI, path="/manage-users")
def get_user_collection_ui(request):
    col = get_user_collection(request)
    return UserCollectionUI(request, col)


@App.path(
    model=UserModelUI,
    path="/manage-users/{username}",
    variables=lambda obj: {"username": obj.model.data["username"]},
)
def get_user_model_ui(request, username):
    user = get_user_collection(request).get_by_username(username)
    if user is None:
        return None
    col = get_user_collection(request)
    return UserModelUI(request, user, UserCollectionUI(request, col))


@App.path(model=CurrentUserModelUI, path="/profile")
def get_current_user_model_ui(request):
    userid = request.identity.userid
    if userid is None:
        return None
    col = get_user_collection(request)
    user = col.get_by_userid(userid)
    if user is None:
        return None
    return CurrentUserModelUI(request, user, UserCollectionUI(request, col))
