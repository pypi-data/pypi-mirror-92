from morpfw.authn.pas.user.rulesprovider import (
    UserRulesProvider as BaseUserRulesProvider,
)
from morpfw.authn.pas.user.model import UserModel
from ..app import App


class UserRulesProvider(BaseUserRulesProvider):
    def validate(self, password: str, check_state: bool = True) -> bool:
        context = self.context
        if check_state and context.data["state"] not in ["new", "active"]:
            return False
        return context.storage.validate(context, context.userid, password)


@App.rulesprovider(model=UserModel)
def get_user_rulesprovider(context):
    return UserRulesProvider(context)
