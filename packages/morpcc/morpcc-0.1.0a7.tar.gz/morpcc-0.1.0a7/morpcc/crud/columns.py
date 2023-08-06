import html

from morpcc.util import permits
from morpfw.crud import permission as crudperm
from morpfw.crud.model import Model

from ..app import App


@App.structure_column(model=Model, name="type")
def get_type_column(model, request, name):
    return str(model.__class__.__name__)


@App.structure_column(model=Model, name="object_string")
def get_objectstring_column(model, request, name):
    return html.escape(str(model))


@App.structure_column(model=Model, name="buttons")
def get_buttons_column(model, request, name):
    typeinfos = request.app.config.type_registry.get_typeinfos(request)
    uiobj = None
    # FIXME: have a nicer API through typeregistry
    if getattr(model, "ui", None):
        uiobj = model.ui()
    else:
        for n, ti in typeinfos.items():
            path_model = getattr(model, "__path_model__", None)
            if model.__class__ == ti["model"] or path_model == ti["model"]:
                uiobj = ti["model_ui"](
                    request, model, ti["collection_ui_factory"](request)
                )
                break

    if uiobj is None:
        raise ValueError("Unable to locate typeinfo for %s" % model)

    buttons = []

    if permits(request, uiobj, crudperm.View):
        buttons.append(
            {
                "icon": "eye",
                "url": request.link(uiobj, "+%s" % uiobj.default_view),
                "title": "View",
            }
        )

    if permits(request, uiobj, crudperm.Edit) and uiobj.update_view_enabled:
        buttons.append(
            {"icon": "edit", "url": request.link(uiobj, "+edit"), "title": "Edit"}
        )

    if permits(request, uiobj, crudperm.Delete) and uiobj.delete_view_enabled:
        buttons.append(
            {
                "icon": "trash",
                "data-url": request.link(uiobj, "+modal-delete"),
                "title": "Delete",
                "class": "modal-link",
            }
        )
    render = request.app.get_template("master/snippet/button-group-sm.pt")
    return render({"buttons": buttons}, request)
