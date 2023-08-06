import morepath
import rulez
from morpfw.authn.pas import permission as authperm
from morpfw.authn.pas.user.model import UserCollection
from morpfw.authz.pas import APIKeyModel, CurrentUserModel, UserModel
from morpfw.crud import permission as crudperms
from morpfw.crud.model import Collection, Model
from morpfw.permission import All

from ..crud.model import CollectionUI, ModelUI
from ..util import permits
from .policy import MorpCCAuthzPolicy

Policy = MorpCCAuthzPolicy


def rule_from_config(request, key, default=True):
    app = request.app
    value = app.get_config(key, default)
    return value


def rule_from_assignment(request, model, permission, identity):
    usercol = request.get_collection("morpfw.pas.user")
    user = usercol.get_by_userid(identity.userid)
    if user["is_administrator"]:
        return True
    pcol = request.get_collection("morpcc.permissionassignment")

    permission_name = "%s:%s" % (permission.__module__, permission.__name__,)

    user_roles = []
    for gid, roles in user.group_roles().items():
        for role in roles:
            role_ref = "%s::%s" % (gid, role)
            user_roles.append(role_ref)

    request.app.resolve_permissionassignment(request, model, permission, identity)

    # find global/site permission
    model_hierarchy = []
    for klass in model.__class__.__mro__:
        model_name = "%s:%s" % (klass.__module__, klass.__name__)
        model_hierarchy.append(model_name)

    for model_name in model_hierarchy:
        found_perms = []
        for perm in pcol.search(
            rulez.and_(
                rulez.field["model"] == model_name,
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

    return False


@Policy.permission_rule(model=UserCollection, permission=authperm.Register)
def allow_api_registration(identity, model, permission):
    return model.request.app.get_config("morpfw.new_registration.enabled", True)


@Policy.permission_rule(model=Collection, permission=All)
def collection_permission(identity, model, permission):
    return rule_from_assignment(model.request, model, permission, identity)


@Policy.permission_rule(model=CollectionUI, permission=All)
def collectionui_permission(identity, model, permission):
    return permits(model.request, model.collection, permission)


@Policy.permission_rule(model=ModelUI, permission=All)
def modelui_permission(identity, model, permission):
    return permits(model.request, model.model, permission)


@Policy.permission_rule(model=Model, permission=All)
def model_permission(identity, model, permission):
    return rule_from_assignment(model.request, model, permission, identity)


def currentuser_permission(identity, model, permission):
    request = model.request
    usercol = request.get_collection("morpfw.pas.user")
    user = usercol.get_by_userid(identity.userid)
    if user["is_administrator"]:
        return True
    userid = identity.userid
    if isinstance(model, UserModel):
        if model.userid == userid:
            return True
    elif isinstance(model, APIKeyModel):
        if model["userid"] == userid:
            return True

    return rule_from_assignment(
        request=model.request, model=model, permission=permission, identity=identity
    )


@Policy.permission_rule(model=UserModel, permission=crudperms.All)
def allow_user_crud(identity, model, permission):
    return currentuser_permission(identity, model, permission)


@Policy.permission_rule(model=UserModel, permission=authperm.ChangePassword)
def allow_change_password(identity, model, permission):
    return currentuser_permission(identity, model, permission)


@Policy.permission_rule(model=CurrentUserModel, permission=authperm.ChangePassword)
def allow_self_change_password(identity, model, permission):
    return currentuser_permission(identity, model, permission)


@Policy.permission_rule(model=APIKeyModel, permission=crudperms.All)
def allow_apikey_management(identity, model, permission):
    return currentuser_permission(identity, model, permission)
