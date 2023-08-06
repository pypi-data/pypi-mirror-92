import html

import deform
import morepath
import rulez
from morpfw.crud import permission as crudperms

from ...app import App
from ...root import Root
from ...util import permits
from ..model import CollectionUI, ModelUI


def _term_search(context, request):
    # FIXME: this need to be secured
    resource_type = request.GET.get("resource_type", "").strip()
    if not resource_type:
        return {}
    value_field = request.GET.get("value_field", "").strip()
    if not value_field:
        return {}
    term_field = request.GET.get("term_field", "").strip()
    if not term_field:
        return {}
    term = request.GET.get("term", "").strip()
    if not term:
        return {}

    typeinfo = request.app.config.type_registry.get_typeinfo(
        name=resource_type, request=request
    )
    col = typeinfo["collection_factory"](request)
    objs = col.search(query={"field": term_field, "operator": "~", "value": term})
    result = {"results": []}
    for obj in objs:
        if permits(request, obj, crudperms.View):
            result["results"].append({"id": obj[value_field], "text": obj[term_field]})
    return result


@App.json(model=Root, name="term-search", permission=crudperms.View)
def root_term_search(context, request):
    return _term_search(context, request)
