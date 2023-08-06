import typing
from dataclasses import dataclass, field
from datetime import datetime

import morpfw
from morpfw.authn.pas.user.model import UserModel
from morpfw.crud.xattrprovider import FieldXattrProvider

from ..app import App


@dataclass
class UserXattrSchema(object):

    firstname: typing.Optional[str] = field(
        default=None, metadata={"title": "First Name"}
    )
    lastname: typing.Optional[str] = field(
        default=None, metadata={"title": "Last Name"}
    )
    displayname: typing.Optional[str] = field(
        default=None, metadata={"title": "Display Name"}
    )
    address: typing.Optional[str] = field(default=None, metadata={"title": "Address"})
    agreed_terms: typing.Optional[bool] = field(
        default=False, metadata={"editable": False}
    )
    agreed_terms_ts: typing.Optional[datetime] = field(
        default=None, metadata={"editable": False}
    )


class UserXattrProvider(FieldXattrProvider):

    schema = UserXattrSchema


@App.xattrprovider(model=UserModel)
def get_xattr_provider(context):
    return UserXattrProvider(context)
