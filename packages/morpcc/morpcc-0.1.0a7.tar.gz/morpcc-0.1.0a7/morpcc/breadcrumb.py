from .app import App
from .crud.model import CollectionUI, ModelUI
from .root import Root

VIEW_TITLES = {"": "Home"}


@App.breadcrumb(model=Root)
def get_root_breadcrumb(model, request):
    view_title = VIEW_TITLES.get(request.view_name, None)
    if not view_title and request.view_name:
        view_title = request.view_name.replace("-", " ").title()
    if view_title:
        return [
            {
                "title": view_title,
                "url": request.link(model, request.view_name),
                "active": True,
            }
        ]
    return []


@App.breadcrumb(model=ModelUI)
def get_model_breadcrumb(model, request):
    view_title = None
    if request.view_name:
        view_title = request.view_name.replace("-", " ").title()

    try:
        typeinfo = request.app.get_typeinfo_by_schema(
            schema=model.model.schema, request=request
        )
    except KeyError as e:
        return []

    collection_crumb = {
        "title": typeinfo["title"],
        "url": request.link(model.collection_ui),
        "active": False,
    }
    model_crumb = {
        "title": model.model.title(),
        "url": request.link(model),
        "active": False,
    }
    crumbs = [collection_crumb, model_crumb]
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


@App.breadcrumb(model=CollectionUI)
def get_collection_breadcrumb(model, request):
    view_title = None
    if request.view_name:
        view_title = request.view_name.replace("-", " ").title()

    try:
        typeinfo = request.app.get_typeinfo_by_schema(
            schema=model.collection.schema, request=request
        )
    except KeyError as e:
        return []

    collection_crumb = {
        "title": typeinfo["title"],
        "url": request.link(model),
        "active": False,
    }
    crumbs = [collection_crumb]
    if view_title:
        return crumbs + [
            {
                "title": view_title,
                "url": request.link(model, "+" + request.view_name),
                "active": True,
            }
        ]

    collection_crumb["active"] = True
    return crumbs
