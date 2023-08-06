import typing
from dataclasses import dataclass, field
from datetime import date, datetime

import deform.widget
from inverter.dc2colander import dc2colander

from .. import permission as perm
from ..app import App


@dataclass
class GeneralSetting(object):

    ldap_enabled: typing.Optional[bool] = field(
        default=False,
        metadata={
            "title": "Enable LDAP",
            "required": False,
            "morpcc.setting.key": "morpcc.ldap.enabled",
        },
    )


@App.setting_page(name="general", title="General", order=-1)
def get_schema(request):
    return GeneralSetting
