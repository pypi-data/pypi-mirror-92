from morpfw.crud import permission as crudperms

from ..app import App
from ..crud.view.view import view as default_view
from .model import UserModelUI


@App.html(
    model=UserModelUI, name="view", permission=crudperms.View, template="auth/user.pt"
)
def view(context, request):
    result = default_view(context, request)
    user = context.model
    username = user["username"]
    xattr = user.xattrprovider()
    if user.get_blob("profile-photo"):
        photo_url = request.link(context, "+download?field=profile-photo")
    else:
        photo_url = request.relative_url("/__static__/morpcc/img/person-icon.jpg")

    result["profilephoto_url"] = photo_url
    return result
