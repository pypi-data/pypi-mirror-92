import colander
import deform
import deform.widget
import morepath
import morpfw.authn.pas.exc
from morpfw.authn.pas.user.path import get_user_collection
from morpfw.crud import permission as crudperm
from morpfw.crud.model import Model
from morpfw.crud.view import get_blob

from ... import permission
from ...app import App
from ..model import ModelUI
from ..tempstore import FSBlobFileUploadTempStore


def upload_form(context: ModelUI, request: morepath.Request) -> deform.Form:
    fields = {}
    model = context.model
    for f in model.blob_fields:
        fields[f] = colander.SchemaNode(
            deform.FileData(),
            missing=colander.drop,
            widget=deform.widget.FileUploadWidget(
                FSBlobFileUploadTempStore(f, context, request, "/tmp/tempstore")
            ),
            oid="file-upload-%s" % f,
        )

    FileUpload = type("FileUpload", (colander.Schema,), fields)
    fs = FileUpload()
    return deform.Form(fs, buttons=("Upload",), formid="upload-form")


@App.html(
    model=ModelUI,
    name="upload",
    permission=crudperm.Edit,
    template="master/crud/form.pt",
)
def upload(context, request):
    data = {}
    for f in context.model.blob_fields:
        blob = context.model.get_blob(f)
        if blob is None:
            continue
        data[f] = {
            "uid": blob.uuid,
            "filename": blob.filename,
            "size": blob.size,
            "mimetype": blob.mimetype,
            "download_url": request.link(context, "+download?field=%s" % f),
            "preview_url": request.link(context, "+blobpreview?field=%s" % f),
        }

    return {
        "page_title": "Upload",
        "form_title": "Upload",
        "form": upload_form(context, request),
        "form_data": data,
    }


@App.html(
    model=ModelUI,
    name="upload",
    permission=crudperm.Edit,
    template="master/simple-form.pt",
    request_method="POST",
)
def process_upload(context, request):
    form = upload_form(context, request)
    controls = list(request.POST.items())

    failed = False
    data = {}
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        failed = True
        form = e
    if not failed:
        for f in context.model.blob_fields:
            if f not in data:
                continue
            filedata = data[f]
            context.model.put_blob(
                f,
                filedata["fp"],
                filename=filedata["filename"],
                mimetype=filedata["mimetype"],
            )
        request.notify("success", "Upload successful", "Files successfully uploaded")
        return morepath.redirect(request.link(context))

    return {
        "page_title": "Upload",
        "form_title": "Upload",
        "form": form,
        "form_data": data if not failed else None,
    }


@App.view(model=ModelUI, name="download", permission=crudperm.View)
def download(context, request):
    return get_blob(context.model, request)
