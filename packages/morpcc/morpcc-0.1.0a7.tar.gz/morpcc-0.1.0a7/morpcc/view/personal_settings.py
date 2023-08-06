import pytz

import colander
import deform
import deform.widget
import morepath
import morpfw.authn.pas.exc
import webob.exc
from inverter import dc2colander
from morpfw.authn.pas.user.path import get_user_collection
from morpfw.crud import permission as crudperm

from .. import permission
from ..app import App
from ..crud.tempstore import FSBlobFileUploadTempStore
from ..root import Root
from ..users.model import CurrentUserModelUI, UserModelUI


def get_user_info_schema(user, request):
    email_widget = None
    email_validator = None
    if user["source"] != "local":
        email_widget = deform.widget.TextInputWidget(template="readonly/textinput")
        email_validator = colander.Email(msg="Invalid e-mail address")

    class UserInfoSchema(colander.MappingSchema):
        username = colander.SchemaNode(
            colander.String(),
            oid="userinfo-username",
            missing="",
            widget=deform.widget.TextInputWidget(template="readonly/textinput"),
        )
        email = colander.SchemaNode(
            colander.String(),
            oid="userinfo-email",
            missing="",
            validator=email_validator,
            widget=email_widget,
        )
        timezone = colander.SchemaNode(
            colander.String(),
            oid="userinfo-timezone",
            widget=deform.widget.Select2Widget(
                values=[(x, x) for x in pytz.all_timezones]
            ),
        )

        state = colander.SchemaNode(
            colander.String(),
            oid="userinfo-state",
            missing="",
            widget=deform.widget.TextInputWidget(template="readonly/textinput"),
        )
        created = colander.SchemaNode(
            colander.DateTime(),
            oid="userinfo-created",
            missing=None,
            widget=deform.widget.DateTimeInputWidget(template="readonly/datetimeinput"),
        )

    return UserInfoSchema()


class PasswordSchema(colander.MappingSchema):
    password_current = colander.SchemaNode(
        colander.String(),
        oid="password-current",
        title="Current password",
        widget=deform.widget.PasswordWidget(),
        missing="",
    )

    password = colander.SchemaNode(
        colander.String(),
        oid="password-new",
        title="New password",
        widget=deform.widget.PasswordWidget(),
        missing="",
        validator=colander.Length(min=8),
    )
    password_confirm = colander.SchemaNode(
        colander.String(),
        oid="password-confirm",
        widget=deform.widget.PasswordWidget(),
        title="Confirm new password",
        missing="",
    )

    def validator(self, node: "PasswordSchema", appstruct: dict):
        if appstruct["password"] != appstruct["password_confirm"]:
            raise colander.Invalid(node["password"], "Password does not match")


class AdminPasswordSchema(colander.MappingSchema):

    password = colander.SchemaNode(
        colander.String(),
        oid="password-new",
        title="New password",
        widget=deform.widget.PasswordWidget(),
        missing="",
        validator=colander.Length(min=8),
    )
    password_confirm = colander.SchemaNode(
        colander.String(),
        oid="password-confirm",
        widget=deform.widget.PasswordWidget(),
        title="Confirm new password",
        missing="",
    )

    def validator(self, node: "PasswordSchema", appstruct: dict):
        if appstruct["password"] != appstruct["password_confirm"]:
            raise colander.Invalid(node["password"], "Password does not match")


def userinfo_form(user, request) -> deform.Form:
    return deform.Form(
        get_user_info_schema(user, request), buttons=("Submit",), formid="userinfo-form"
    )


def attributes_form(context, request, mode="edit") -> deform.Form:
    schema = context.xattrprovider().schema
    formschema = dc2colander.convert(
        schema,
        request=request,
        default_tzinfo=request.timezone(),
        mode=mode,
        exclude_fields=["agreed_terms", "agreed_terms_ts"],
    )
    fs = formschema()
    fs = fs.bind(context=context, request=request)
    return deform.Form(fs, buttons=("Submit",), formid="personalinfo-form")


def password_form(request) -> deform.Form:
    userid = request.identity.userid
    users = request.get_collection("morpfw.pas.user")
    user = users.get_by_userid(userid)
    if user["is_administrator"]:
        return deform.Form(
            AdminPasswordSchema(), buttons=("Change password",), formid="password-form"
        )
    return deform.Form(
        PasswordSchema(), buttons=("Change password",), formid="password-form"
    )


def upload_form(context, request) -> deform.Form:
    tempstore = FSBlobFileUploadTempStore(
        "profile-photo", context, request, "/tmp/tempstore"
    )

    class FileUpload(colander.Schema):
        upload = colander.SchemaNode(
            deform.FileData(),
            missing=colander.drop,
            widget=deform.widget.FileUploadWidget(tempstore),
            oid="file-upload",
        )

    return deform.Form(FileUpload(), buttons=("Upload",), formid="upload-form")


@App.html(
    model=UserModelUI,
    name="edit",
    template="master/personal-settings.pt",
    permission=crudperm.Edit,
)
def profile(context, request: morepath.Request):
    user = context.model
    has_photo = user.get_blob("profile-photo")
    forms = [
        {
            "form_title": "Personal Information",
            "form": attributes_form(user, request),
            "readonly": False,
            "form_data": user.data["xattrs"],
        },
        {
            "form_title": "User Information",
            "form": userinfo_form(user, request),
            "readonly": False,
            "form_data": user.data.as_dict(),
        },
    ]
    if user["source"] == "local":
        forms.append(
            {
                "form_title": "Password",
                "form": password_form(request),
                "readonly": False,
            }
        )

    return {
        "page_title": "Profile",
        "profile_photo": request.link(context, "+download?field=profile-photo")
        if has_photo
        else None,
        "forms": forms,
    }


@App.html(
    model=UserModelUI,
    name="edit",
    request_method="POST",
    template="master/personal-settings.pt",
    permission=crudperm.Edit,
)
def process_profile(context, request):
    userinfo_f = userinfo_form(context.model, request)
    password_f = password_form(request)
    controls = list(request.POST.items())
    controls_dict = dict(controls)
    active_form = controls_dict["__formid__"]

    user = context.model

    attributes_f = attributes_form(user, request, mode="edit-process")

    failed = False
    if active_form == "userinfo-form":
        try:
            data = userinfo_f.validate(controls)
        except deform.ValidationFailure as e:
            failed = True
            userinfo_f = e
            userdata = userinfo_f.field.schema.serialize(user.data.as_dict())
            for k in userdata.keys():
                if userinfo_f.cstruct[k] is not colander.null:
                    userdata[k] = userinfo_f.cstruct[k]
            userinfo_f.field.cstruct = userdata

        if not failed:
            updatedata = {}
            for f in ["email", "timezone"]:
                if user["source"] != "local" and f == "email":
                    continue
                updatedata[f] = data[f]
            user.update(updatedata)

        if not failed:
            request.notify(
                "success",
                "Profile updated",
                "Your profile have been successfully updated",
            )
            return morepath.redirect(request.url)
    elif active_form == "password-form":
        if user["source"] != "local":
            raise webob.exc.HTTPUnprocessableEntity(
                "Password change form is only available for local users"
            )
        try:
            data = password_f.validate(controls)
        except deform.ValidationFailure as e:
            failed = True
            password_f = e

        if not failed:
            users = request.get_collection("morpfw.pas.user")
            current_user = users.get_by_userid(request.identity.userid)
            if not current_user["is_administrator"] and not user.validate(
                data["password_current"]
            ):
                exc = colander.Invalid(password_f, "Invalid password")
                password_f.widget.handle_error(password_f, exc)
                failed = True

        if not failed:
            try:
                user.change_password(
                    data.get("password_current", ""), data["password"], secure=False
                )
            except morpfw.authn.pas.exc.InvalidPasswordError as e:
                exc = colander.Invalid(password_f, "Invalid password")
                password_f.widget.handle_error(password_f, exc)
                failed = True

        if not failed:
            request.notify(
                "success",
                "Password changed",
                "Your password have been successfully changed",
            )
            return morepath.redirect(request.url)
        else:
            request.notify(
                "error", "Password change failed", "Unable to change password"
            )
    elif active_form == "personalinfo-form":
        try:
            data = attributes_f.validate(controls)
        except deform.ValidationFailure as e:
            failed = True
            attributes_f = e

        if not failed:
            xattrprovider = user.xattrprovider()
            xattrprovider.update(data)
            request.notify(
                "success",
                "Profile updated",
                "Your profile have been successfully updated",
            )
            return morepath.redirect(request.url)

    else:
        request.notify("error", "Unknown form", "Invalid form identifier was supplied")

        return morepath.redirect(request.url)

    has_photo = user.get_blob("profile-photo")
    return {
        "page_title": "Personal Settings",
        "profile_photo": request.link(context, "+download?field=profile-photo")
        if has_photo
        else None,
        "forms": [
            {
                "form_title": "Personal Information",
                "form": attributes_f,
                "readonly": False,
                "form_data": user["xattrs"]
                if active_form != "personalinfo-form"
                else None,
            },
            {
                "form_title": "User Information",
                "form": userinfo_f,
                "readonly": False,
                "form_data": user.data.as_dict()
                if active_form != "userinfo-form"
                else None,
            },
            {"form_title": "Password", "form": password_f, "readonly": False,},
        ],
    }
