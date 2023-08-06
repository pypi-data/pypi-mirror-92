import rulez
from morpfw.crud import permission as crudperm

from ...app import App
from ...deform.referencewidget import ReferenceWidget
from ..model import CollectionUI, ModelUI
from .listing import datatable_search


def _reference_content_search(context, request, request_method="GET"):
    bref_name = request.GET.get("backreference_name", "").strip()
    if not bref_name:
        return {}

    brefs = context.model.backreferences()
    bref = brefs[bref_name]
    collectionui = bref.collection(request).ui()

    ref = bref.get_reference(request)
    return datatable_search(
        collectionui,
        request,
        additional_filters=rulez.field(ref.name) == context.model[ref.attribute],
        request_method=request_method,
    )


@App.json(model=ModelUI, name="backreference-search.json", permission=crudperm.View)
def reference_content_search(context, request):
    return _reference_content_search(context, request)


@App.json(
    model=ModelUI,
    name="backreference-search.json",
    permission=crudperm.View,
    request_method="POST",
)
def reference_content_search_port(context, request):
    return _reference_content_search(context, request, request_method="POST")

