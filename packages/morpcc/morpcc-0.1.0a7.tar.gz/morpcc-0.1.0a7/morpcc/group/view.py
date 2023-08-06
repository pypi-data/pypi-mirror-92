import html
import typing
from dataclasses import dataclass, field

import colander
import deform.widget
import morepath
from inverter import dc2colander
from morpfw.authn.pas.group.model import DEFAULT_VALID_ROLES
from morpfw.crud import permission as crudperms
from morpfw.crud.errors import AlreadyExistsError, ValidationError

from ..app import App
from .model import GroupModelUI


def member_select_widget(request):
    usercol = request.get_collection("morpfw.pas.user")
    choices = []
    for user in usercol.all():
        if user["state"] in ["active", "inactive"]:
            choices.append((user.userid, user["username"]))
    return deform.widget.Select2Widget(values=choices, multiple=True)


def group_schema(context, request):

    valid_roles = request.app.get_config("morpfw.valid_roles", DEFAULT_VALID_ROLES)
    roles_c = len(valid_roles)

    class RoleAssignment(colander.Schema):
        role = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.TextInputWidget(template="textinput-noedit"),
        )
        members = colander.SchemaNode(
            colander.List(), widget=member_select_widget(request)
        )

    class Roles(colander.SequenceSchema):
        roles = RoleAssignment()

    class GroupForm(colander.Schema):
        groupname = colander.SchemaNode(
            colander.String(),
            missing=colander.drop,
            widget=deform.widget.TextInputWidget(template="readonly/textinput"),
        )
        memberships = Roles(
            widget=deform.widget.SequenceWidget(min_len=roles_c, max_len=roles_c)
        )

    return GroupForm()


@App.html(
    model=GroupModelUI,
    name="edit",
    permission=crudperms.Edit,
    template="master/crud/form.pt",
)
def edit(context, request):
    schema = group_schema(context, request)
    form = deform.Form(schema, buttons=("Submit",))
    role_members = {}
    for role in request.app.get_config("morpfw.valid_roles", DEFAULT_VALID_ROLES):
        role_members.setdefault(role, [])

    for member in context.model.members():
        for role in context.model.get_member_roles(member.userid):
            if role not in role_members:
                continue
            role_members[role].append(member.userid)

    memberships = [{"role": r, "members": m} for r, m in role_members.items()]
    data = {
        "groupname": context.model["groupname"],
        "memberships": memberships,
    }

    return {
        "page_title": "Edit %s" % html.escape(str(context.model.__class__.__name__)),
        "form_title": "Edit",
        "form": form,
        "form_data": data,
    }


@App.html(
    model=GroupModelUI,
    name="edit",
    permission=crudperms.Edit,
    template="master/crud/form.pt",
    request_method="POST",
)
def process_edit(context, request):
    fs = group_schema(context, request)
    controls = list(request.POST.items())
    form = deform.Form(fs, buttons=("Submit",))

    failed = False
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True

    if not failed:
        try:
            context.model.remove_members([m.userid for m in context.model.members()])
            for m in data["memberships"]:
                for member_id in m["members"]:
                    context.model.grant_member_role(member_id, m["role"])
        except ValidationError as e:
            failed = True
            for fe in e.field_errors:
                node = form
                if fe.path in form:
                    node = form[fe.path]
                node_error = colander.Invalid(node.widget, fe.message)
                node.widget.handle_error(node, node_error)
        if not failed:
            return morepath.redirect(request.link(context))

    @request.after
    def set_header(response):
        response.headers.add("X-MORP-FORM-FAILED", "True")

    return {
        "page_title": "Edit %s" % html.escape(str(context.model.__class__.__name__)),
        "form_title": "Edit",
        "form": form,
    }
