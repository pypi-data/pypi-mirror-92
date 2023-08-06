import typing
from dataclasses import dataclass

import morpfw


@dataclass
class SettingSchema(morpfw.Schema):

    key: typing.Optional[str] = None
    data: typing.Optional[dict] = None
