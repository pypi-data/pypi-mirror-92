from dataclasses import dataclass

import morpfw
from morpfw.authn.pas.user.model import UserModel

from ..app import App


class UserStateMachine(morpfw.StateMachine):

    states = ["new", "active", "inactive"]
    transitions = [
        {
            "trigger": "initialize",
            "source": "new",
            "dest": "active",
            "conditions": ["is_validated"],
        },
        {"trigger": "activate", "source": "inactive", "dest": "active"},
        {"trigger": "deactivate", "source": "active", "dest": "inactive"},
    ]

    def is_validated(self):
        xattr = self._context.xattrprovider()
        if self._request.app.get_config("morpcc.registration_verify_email", False):
            email_validated = xattr.get("morpcc.email.validated", False)
            return email_validated
        return True


@App.statemachine(model=UserModel)
def userstatemachine(context):
    return UserStateMachine(context)
