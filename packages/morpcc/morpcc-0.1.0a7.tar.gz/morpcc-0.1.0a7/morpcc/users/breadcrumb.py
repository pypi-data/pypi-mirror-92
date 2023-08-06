from ..app import App
from .model import CurrentUserModelUI


@App.breadcrumb(model=CurrentUserModelUI)
def get_profile_breadcrumb(model, request):
    view_title = None
    if request.view_name:
        view_title = request.view_name.replace("-", " ").title()

    model_crumb = {
        "title": "Profile",
        "url": request.link(model),
        "active": False,
    }
    crumbs = [model_crumb]
    if view_title:
        return crumbs + [
            {
                "title": view_title,
                "url": request.link(model, "+" + request.view_name),
                "active": True,
            }
        ]

    model_crumb["active"] = True
    return crumbs
