import typing
from dataclasses import dataclass, field

import morpfw

from ..deform.referencewidget import ReferenceWidget


@dataclass
class ActivityLogSchema(morpfw.Schema):

    userid: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "uuid",
            "deform.widget": ReferenceWidget(
                "morpfw.pas.user", term_field="username", value_field="uuid"
            ),
        },
    )
    source_ip: typing.Optional[str] = None
    resource_type: typing.Optional[str] = None
    resource_uuid: typing.Optional[str] = field(
        default=None, metadata={"format": "uuid"}
    )
    view_name: typing.Optional[str] = None
    activity: typing.Optional[str] = None
