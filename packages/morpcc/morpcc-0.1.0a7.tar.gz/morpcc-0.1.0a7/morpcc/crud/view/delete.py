import html

import deform
import morepath
from inverter import dc2colander
from morpfw.crud import permission as crudperms
from webob.exc import HTTPNotFound

from ...app import App
from ..model import CollectionUI, ModelUI


@App.html(
    model=ModelUI,
    name="delete",
    template="master/crud/delete.pt",
    permission=crudperms.Delete,
)
def delete(context, request):
    if not context.delete_view_enabled:
        raise HTTPNotFound()
    formschema = dc2colander.convert(
        context.model.schema,
        request=request,
        include_fields=context.view_include_fields,
        exclude_fields=context.view_exclude_fields,
        default_tzinfo=request.timezone(),
    )
    data = context.model.data.as_dict()
    return {
        "page_title": "Delete Confirmation",
        "form_title": "Are you sure you want to delete this?",
        "form": deform.Form(formschema()),
        "form_data": data,
    }


@App.html(
    model=ModelUI,
    name="modal-delete",
    template="master/crud/modal-delete.pt",
    permission=crudperms.Delete,
)
def modal_delete(context, request):
    return delete(context, request)


@App.html(
    model=ModelUI,
    name="delete",
    template="master/crud/delete.pt",
    permission=crudperms.Delete,
    request_method="POST",
)
def process_delete(context, request):
    if not context.delete_view_enabled:
        raise HTTPNotFound()
    context.model.delete()
    return morepath.redirect(request.link(context.collection_ui))


@App.html(
    model=ModelUI,
    name="modal-delete",
    template="master/crud/modal-delete.pt",
    permission=crudperms.Delete,
    request_method="POST",
)
def modal_process_delete(context, request):
    if not context.delete_view_enabled:
        raise HTTPNotFound()
    context.model.delete()
    return morepath.redirect(request.link(context.collection_ui, "+modal-close"))
