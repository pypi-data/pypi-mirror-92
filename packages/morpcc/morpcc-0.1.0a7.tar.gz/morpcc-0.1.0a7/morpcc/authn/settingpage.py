import typing
from dataclasses import dataclass, field
from urllib.parse import urlparse

import deform.widget
from morpfw.colander import EncryptedExportField

from ..app import App


def get_encrypted_field(request):
    key = request.app.get_config("morpfw.secret.fernet_key")
    return EncryptedExportField(key)


def valid_dn(request, schema, field, value, mode=None):
    if "=" not in value:
        return "Invalid DN"


def valid_ldapurl(request, schema, field, value, mode=None):
    try:
        parsed = urlparse(value)
    except:
        return "Invalid URI"
    if parsed.scheme.lower() not in ["ldap", "ldaps"]:
        return "Invalid URI"


@dataclass
class LDAPSetting(object):

    ldap_uri: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "LDAP URI",
            "description": "LDAP connection URI (eg: ldap://ldap.service.local)",
            "morpcc.setting.key": "morpcc.ldap.uri",
            "required": True,
            "validators": [valid_ldapurl]
        },
    )
    use_tls: typing.Optional[bool] = field(
        default=False,
        metadata={
            "title": "Use TLS",
            "required": False,
            "morpcc.setting.key": "morpcc.ldap.use_tls",
        },
    )
    bind_dn: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Bind DN",
            "description": "DN to bind as",
            "morpcc.setting.key": "morpcc.ldap.bind_dn",
            "required": True,
            "validators": [valid_dn],
        },
    )
    bind_password: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Bind Password",
            "description": "Bind Password",
            "deform.widget": deform.widget.PasswordWidget(redisplay=True),
            "morpcc.setting.key": "morpcc.ldap.bind_password",
            "morpcc.setting.colander_field_factory": get_encrypted_field,
            "required": True,
        },
    )
    user_base_dn: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "User Base DN",
            "description": "Base DN where all users are stored",
            "morpcc.setting.key": "morpcc.ldap.user_base_dn",
            "required": True,
            "validators": [valid_dn],
        },
    )

    user_search_filter: typing.Optional[str] = field(
        default=r"(&(objectClass=inetOrgPerson)(uid={username}))",
        metadata={
            "title": "LDAP User Search Filter",
            "morpcc.setting.key": "morpcc.ldap.user_search_filter",
            "required": True,
        },
    )
    user_search_scope: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "LDAP User Search Scope",
            "description": "Search scope of for user lookup",
            "morpcc.setting.key": "morpcc.ldap.user_search_scope",
            "required": True,
            "deform.widget": deform.widget.SelectWidget(
                values=[
                    ("base", "Base DN"),
                    ("onelevel", "Single Level"),
                    ("subtree", "Subtree"),
                ]
            ),
        },
    )
    username_attr: typing.Optional[str] = field(
        default="uid",
        metadata={
            "title": "Username Attribute",
            "description": "LDAP attribute to use as login username",
            "morpcc.setting.key": "morpcc.ldap.username_attr",
            "required": True,
        },
    )
    email_attr: typing.Optional[str] = field(
        default="mail",
        metadata={
            "title": "Email Attribute",
            "description": "LDAP attribute to use for getting email address",
            "morpcc.setting.key": "morpcc.ldap.email_attr",
            "required": True,
        },
    )


@App.setting_page(name="ldap", title="LDAP Settings")
def get_schema(request):
    scol = request.get_collection("morpcc.setting")
    enabled_setting = scol.get_by_key("morpcc.ldap.enabled")
    enabled = bool(enabled_setting["data"]["value"])
    if enabled:
        return LDAPSetting
