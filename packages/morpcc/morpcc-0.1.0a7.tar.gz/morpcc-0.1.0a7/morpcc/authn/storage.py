import ldap
from morpfw.authn.pas.storage.ldap3storage import LDAP3SQLUserStorage
from morpfw.authn.pas.storage.sqlstorage import UserSQLStorage
from morpfw.authn.pas.user.model import UserModel

from ..app import App

_scopes = {
    "base": ldap.SCOPE_BASE,
    "onelevel": ldap.SCOPE_ONELEVEL,
    "subtree": ldap.SCOPE_SUBTREE,
}


@App.storage(model=UserModel)
def get_user_sqlstorage(model, request, blobstorage):
    settings = request.get_collection("morpcc.setting")
    if not settings.resolve_raw("morpcc.ldap.enabled", None):
        return UserSQLStorage(request, blobstorage=blobstorage)
    ldap_uri = settings.resolve_raw("morpcc.ldap.uri", None)
    use_tls = settings.resolve_raw("morpcc.ldap.use_tls", None)
    bind_dn = settings.resolve_raw("morpcc.ldap.bind_dn", None)
    bind_password = settings.resolve_raw("morpcc.ldap.bind_password", None)
    if bind_password:
        bind_password = request.fernet_decrypt(bind_password)
    base_dn = settings.resolve_raw("morpcc.ldap.user_base_dn", None)
    search_filter = settings.resolve_raw("morpcc.ldap.user_search_filter", None)
    search_scope = settings.resolve_raw("morpcc.ldap.user_search_scope", None)
    search_scope = _scopes.get(search_scope, None)
    username_attr = settings.resolve_raw("morpcc.ldap.username_attr", None)
    email_attr = settings.resolve_raw("morpcc.ldap.email_attr", None)
    reqcheck = [ldap_uri, bind_dn, bind_password, base_dn, search_filter, search_scope]
    if None in reqcheck:
        print(reqcheck)
        if not request.environ.get("morpcc.ldap.configerror.notified", False):
            request.notify(
                "error",
                "LDAP Configuration Error",
                "There are issues with your LDAP configuration",
            )
            request.environ["morpcc.ldap.configerror.notified"] = True
        return UserSQLStorage(request, blobstorage=blobstorage)

    try:
        return LDAP3SQLUserStorage(
            request,
            ldap_uri=ldap_uri,
            base_dn=base_dn,
            bind_dn=bind_dn,
            bind_password=bind_password,
            start_tls=use_tls,
            search_scope=search_scope,
            username_attr=username_attr,
            email_attr=email_attr,
            filterstr=search_filter,
            blobstorage=blobstorage,
        )
    except ldap.INVALID_CREDENTIALS:
        if not request.environ.get("morpcc.ldap.credentialerror.notified", False):
            request.notify("error", "LDAP connection failed", "Invalid credentials")
            request.environ["morpcc.ldap.credentialerror.notified"] = True

        return UserSQLStorage(request, blobstorage=blobstorage)
    except ldap.PROTOCOL_ERROR:
        if not request.environ.get("morpcc.ldap.protoerror.notified", False):
            request.notify("error", "LDAP connection failed", "Unsupported protocol")
            request.environ["morpcc.ldap.protoerror.notified"] = True

        return UserSQLStorage(request, blobstorage=blobstorage)
