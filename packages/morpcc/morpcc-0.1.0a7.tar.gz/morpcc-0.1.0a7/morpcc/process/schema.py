import typing
from dataclasses import dataclass, field
from datetime import datetime

import morpfw

from ..deform.codewidget import CodeWidget, JSONCodeWidget


@dataclass
class ProcessSchema(morpfw.Schema):

    signal: typing.Optional[str] = field(
        default=None, metadata={"required": True, "editable": False, "searchable": True}
    )
    task_id: typing.Optional[str] = field(
        default=None, metadata={"format": "uuid", "required": True, "editable": False}
    )
    start: typing.Optional[datetime] = field(default=None, metadata={"editable": False})
    end: typing.Optional[datetime] = field(default=None, metadata={"editable": False})
    params: typing.Optional[dict] = field(
        default_factory=dict,
        metadata={"editable": False, "deform.widget": JSONCodeWidget()},
    )
    traceback: typing.Optional[str] = field(
        default=None,
        metadata={
            "format": "text/python",
            "required": False,
            "editable": False,
            "deform.widget": CodeWidget(syntax="pytb"),
        },
    )

    __unique_constraint__ = ["task_id"]
