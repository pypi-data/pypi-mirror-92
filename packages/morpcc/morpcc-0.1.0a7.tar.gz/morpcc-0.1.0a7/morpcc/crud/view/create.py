import html

import colander
import deform
import morepath
from deform.widget import HiddenWidget
from inverter import dc2colander
from morpfw.crud import permission as crudperms
from morpfw.crud.errors import AlreadyExistsError, ValidationError
from webob.exc import HTTPFound, HTTPNotFound

from ...app import App
from ..model import CollectionUI, ModelUI


@App.html(
    model=CollectionUI,
    name="create",
    template="master/simple-form.pt",
    permission=crudperms.Create,
)
def create(context, request):
    if not context.create_view_enabled:
        raise HTTPNotFound()
    default_value_fields = list(request.GET.keys())
    formschema = dc2colander.convert(
        context.collection.schema,
        request=request,
        include_fields=context.create_include_fields,
        exclude_fields=context.create_exclude_fields,
        hidden_fields=default_value_fields,
        default_tzinfo=request.timezone(),
    )
    fs = formschema()
    fs = fs.bind(context=context, request=request)

    form_data = {}
    for f in default_value_fields:
        form_data[f] = request.GET.get(f)

    return {
        "page_title": "Create %s"
        % html.escape(
            str(context.collection.__class__.__name__.replace("Collection", ""))
        ),
        "form_title": "Create",
        "form": deform.Form(fs, buttons=("Submit",)),
        "form_data": form_data,
    }


@App.html(
    model=CollectionUI,
    name="modal-create",
    template="master/crud/modal-form.pt",
    permission=crudperms.Create,
)
def modal_create(context, request):
    return create(context, request)


@App.html(
    model=CollectionUI,
    name="create",
    template="master/simple-form.pt",
    permission=crudperms.Create,
    request_method="POST",
)
def process_create(context, request):
    if not context.create_view_enabled:
        raise HTTPNotFound()
    default_value_fields = list(request.GET.keys())
    formschema = dc2colander.convert(
        context.collection.schema,
        request=request,
        include_fields=context.create_include_fields,
        exclude_fields=context.create_exclude_fields,
        hidden_fields=default_value_fields,
        default_tzinfo=request.timezone(),
    )
    fs = formschema()
    fs = fs.bind(context=context, request=request)

    controls = list(request.POST.items())
    form = deform.Form(fs, buttons=("Submit",))

    failed = False
    data = {}
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True
    if not failed:
        try:
            obj = context.collection.create(data, deserialize=False)
        except AlreadyExistsError as e:
            failed = True
            form_error = colander.Invalid(
                form.widget, "Object with {} already exists".format(e.message)
            )
            form.widget.handle_error(form, form_error)

        if not failed:
            return morepath.redirect(
                request.link(context.modelui_class(request, obj, context))
            )

    @request.after
    def set_header(response):
        response.headers.add("X-MORP-FORM-FAILED", "True")

    return {
        "page_title": "Create %s"
        % html.escape(
            str(context.collection.__class__.__name__.replace("Collection", ""))
        ),
        "form_title": "Create",
        "form": form,
        "form_data": data,
    }


@App.html(
    model=CollectionUI,
    name="modal-create",
    template="master/crud/modal-form.pt",
    permission=crudperms.Create,
    request_method="POST",
)
def modal_process_create(context, request):
    result = process_create(context, request)

    if isinstance(result, HTTPFound):
        return morepath.redirect(request.link(context, "+modal-close"))
    return result
