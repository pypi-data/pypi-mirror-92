import typing
from dataclasses import dataclass, field

import deform.widget
import morpfw

from ..permissionassignment.schema import (
    group_select_widget,
    permission_select_widget,
    roles_select_widget,
    user_select_widget,
)


@dataclass
class ObjectPermissionAssignmentSchema(morpfw.Schema):

    object_uuid: typing.Optional[str] = field(
        default=None, metadata={"format": "uuid", "index": True}
    )
    permission: typing.Optional[str] = field(
        default=None,
        metadata={
            "title": "Permission",
            "deform.widget_factory": permission_select_widget,
        },
    )

    roles: typing.Optional[list] = field(
        default_factory=list, metadata={"deform.widget_factory": roles_select_widget}
    )

    rule: typing.Optional[str] = field(
        default="allow",
        metadata={
            "required": True,
            "deform.widget": deform.widget.SelectWidget(
                values=[("allow", "Allow"), ("reject", "Reject")]
            ),
        },
    )

    enabled: typing.Optional[bool] = True
