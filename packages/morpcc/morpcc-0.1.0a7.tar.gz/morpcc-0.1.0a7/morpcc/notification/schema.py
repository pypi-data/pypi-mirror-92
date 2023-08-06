import typing
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import morpfw
from morpcc.deform.referencewidget import UserReferenceWidget

from ..deform.codewidget import JSONCodeWidget


def default_user(request, data, model):
    if data["userid"]:
        return data["userid"]
    return request.identity.userid


@dataclass
class NotificationSchema(morpfw.Schema):

    icon: typing.Optional[str] = "bell"
    subject: typing.Optional[str] = None
    message: typing.Optional[str] = None
    link: typing.Optional[dict] = field(
        default_factory=dict, metadata={"deform.widget": JSONCodeWidget(),}
    )
    link_label: typing.Optional[str] = None
    userid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "deform.widget": UserReferenceWidget(),
            "compute_value": default_user,
        },
    )
    read: typing.Optional[datetime] = None
