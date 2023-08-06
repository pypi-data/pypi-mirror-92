import rulez
from morpcc.authz import rule_from_assignment
from morpfw.crud import permission as crudperm
from morpfw.crud.model import Collection, Model
from morpfw.permission import All as MFWAll

from .app import App
from .crud.model import CollectionUI, ModelUI
from .root import Root
from .users.model import CurrentUserModelUI


@App.permission_rule(model=Root, permission=MFWAll)
def root_view_permission(identity, model, permission):
    return rule_from_assignment(model.request, model, permission, identity)


@App.permission_resolver()
def resolve_model_permission(request, model, permission, identity):
    usercol = request.get_collection("morpfw.pas.user")
    user = usercol.get_by_userid(identity.userid)

    user_roles = []
    for gid, roles in user.group_roles().items():
        for role in roles:
            role_ref = "%s::%s" % (gid, role)
            user_roles.append(role_ref)
            
    permission_name = "%s:%s" % (permission.__module__, permission.__name__,)
    opcol = request.get_collection("morpcc.objectpermissionassignment")
    # find object permission
    if isinstance(model, Model) or isinstance(model, ModelUI):
        found_perms = []
        for perm in opcol.search(
            rulez.and_(
                rulez.field["object_uuid"] == model.uuid,
                rulez.field["permission"] == permission_name,
                rulez.field["enabled"] == True,
            )
        ):
            found_perms.append(perm)

        for perm in sorted(
            found_perms, key=lambda x: 0 if x["rule"] == "reject" else 1
        ):
            for role in user_roles:
                if role in (perm["roles"] or []):
                    if perm["rule"] == "allow":
                        return True
                    return False

