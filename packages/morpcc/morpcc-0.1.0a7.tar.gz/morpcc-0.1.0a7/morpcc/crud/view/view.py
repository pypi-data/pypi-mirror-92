import html
import json
from urllib.parse import urlencode

import deform
import deform.widget
import morepath
import morpfw
from inverter import dc2colander
from morpfw.crud import permission as crudperms

from ...app import App
from ...deform.referencewidget import ReferenceWidget
from ..model import CollectionUI, ModelUI


@App.view(model=CollectionUI)
def collection_index(context, request):
    return morepath.redirect(request.link(context, "+%s" % context.default_view))


@App.view(model=ModelUI)
def model_index(context, request):
    return morepath.redirect(request.link(context, "+%s" % context.default_view))


def base_view(context, request):
    formschema = dc2colander.convert(
        context.model.schema,
        request=request,
        include_fields=context.view_include_fields,
        exclude_fields=context.view_exclude_fields,
        default_tzinfo=request.timezone(),
    )

    xattrprovider = context.model.xattrprovider()
    if xattrprovider:
        xattrformschema = dc2colander.convert(
            xattrprovider.schema,
            request=request,
            default_tzinfo=request.timezone(),
            exclude_fields=["agreed_terms", "agreed_terms_ts"],
        )
    else:
        xattrformschema = None
    data = context.model.data.as_dict()
    sm = context.model.statemachine()

    metadataschema = dc2colander.convert(
        morpfw.Schema,
        request=request,
        exclude_fields=["blobs", "xattrs"],
        default_tzinfo=request.timezone(),
    )
    # FIXME: widget override should be part of dc2colander
    for f in metadataschema.__all_schema_nodes__:
        if f.name == "creator":
            f.widget = ReferenceWidget(
                "morpfw.pas.user", term_field="username", value_field="uuid"
            )
    if sm:
        triggers = [
            i for i in sm._machine.get_triggers(sm.state) if not i.startswith("to_")
        ]
    else:
        triggers = None

    fs = formschema()
    fs = fs.bind(context=context, request=request)

    mfs = metadataschema(
        widget=deform.widget.FormWidget(
            readonly_template="readonly/form_inline",
            readonly_item_template="readonly/mapping_item_inline",
        )
    )
    mfs = mfs.bind(context=context, request=request)

    xfs = None
    if xattrprovider:
        xfs = xattrformschema()
        xfs = xfs.bind(context=context, request=request)

    return {
        "page_title": "View: %s" % html.escape(context.model.title()),
        "form_title": "View",
        "content": context,
        "metadataform": deform.Form(mfs),
        "form": deform.Form(fs),
        "form_data": data,
        "xattrform": deform.Form(xfs) if xattrprovider else None,
        "xattrform_data": xattrprovider.as_dict() if xattrprovider else None,
        "readonly": True,
        "transitions": triggers,
    }


@App.html(
    model=ModelUI,
    name="view",
    template="master/crud/view.pt",
    permission=crudperms.View,
)
def view(context, request):
    result = base_view(context, request)
    result["references"] = []
    for refname, ref in context.model.references().items():
        refmodel = context.model.resolve_reference(ref)
        if refmodel:
            refmodelui = refmodel.ui()
            refdata = base_view(refmodelui, request)
            refdata["name"] = ref.name
            refdata["title"] = ref.get_title(request)
            refdata["content"] = refmodelui
            result["references"].append(refdata)

    result["single_backreferences"] = []
    result["backreferences"] = []
    for refname, bref in context.model.backreferences().items():
        columns = []
        column_options = []
        collectionui = bref.collection(request).ui()
        ref = bref.get_reference(request)
        for col in collectionui.columns:
            columns.append(col["title"])
            column_options.append(col)
        columns_order = collectionui.columns_order
        create_default = {bref.reference_name: context[ref.attribute]}
        create_default_qs = urlencode(create_default)
        create_link = request.link(collectionui, "+create?%s" % create_default_qs)
        modal_create_link = request.link(
            collectionui, "+modal-create?%s" % create_default_qs
        )
        datatable_method = "GET"
        if len(columns) > 7:
            datatable_method = "POST"
        brefdata = {
            "name": bref.name,
            "title": bref.get_title(request),
            "single_reference": bref.single_reference,
            "datatable_url": request.link(
                context,
                "backreference-search.json?backreference_name={}".format(bref.name),
            ),
            "datatable_method": datatable_method,
            "columns": columns,
            "column_options": json.dumps(column_options),
            "columns_order": json.dumps(columns_order),
            "create_link": create_link,
            "modal_create_link": modal_create_link,
        }

        if bref.single_reference:
            content = context.model.resolve_backreference(bref)
            if content:
                item = content[0]
                itemui = item.ui()
                formschema = dc2colander.convert(
                    item.schema,
                    request=request,
                    include_fields=itemui.view_include_fields,
                    exclude_fields=itemui.view_exclude_fields,
                    default_tzinfo=request.timezone(),
                )
                fs = formschema()
                fs = fs.bind(context=item, request=request)
                brefdata["form"] = deform.Form(fs)
                brefdata["form_data"] = item.as_dict()
                brefdata["content"] = item.ui()
            result["single_backreferences"].append(brefdata)
        else:
            result["backreferences"].append(brefdata)

    return result


@App.html(
    model=ModelUI, name="preview", permission=crudperms.View,
)
def preview(context, request):
    formschema = dc2colander.convert(
        context.model.schema,
        request=request,
        include_fields=context.view_include_fields,
        exclude_fields=context.view_exclude_fields,
        default_tzinfo=request.timezone(),
    )

    fs = formschema()
    fs = fs.bind(context=context, request=request)
    form = deform.Form(fs)
    form_data = context.model.data.as_dict()
    return form.render(
        appstruct=form_data, readonly=True, request=request, context=context
    )


@App.html(
    model=ModelUI,
    name="modal-view",
    template="master/crud/modal-view.pt",
    permission=crudperms.View,
)
def modal_view(context, request):
    return view(context, request)


@App.html(
    model=ModelUI,
    name="modal-close",
    template="master/crud/modal-close.pt",
    permission=crudperms.View,
)
def modal_close(context, request):
    return {}


@App.html(
    model=CollectionUI,
    name="modal-close",
    template="master/crud/modal-close.pt",
    permission=crudperms.View,
)
def collection_modal_close(context, request):
    return {}


@App.view(
    model=ModelUI, name="statemachine", permission=crudperms.Edit, request_method="POST"
)
def statemachine(context, request):
    transition = request.POST.get("transition", None)
    sm = context.model.statemachine()
    if transition:
        attr = getattr(sm, transition, None)
        if attr:
            attr()
            request.notify("success", "State updated", "Object state have been updated")
            return morepath.redirect(request.link(context))
    request.notify(
        "error", "Unknown transition", 'Transition "%s" is unknown' % transition
    )
    return morepath.redirect(request.link(context))
