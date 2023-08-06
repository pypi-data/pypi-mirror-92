from uuid import uuid4

import morepath
from more.itsdangerous import IdentityPolicy as BaseItsDangerousIdentityPolicy
from morpfw.authn.pas.policy import Identity, JWTWithAPIKeyIdentityPolicy


class ItsDangerousIdentityPolicy(BaseItsDangerousIdentityPolicy):
    def __init__(self, *args, **kwargs):
        if "secret" in kwargs:
            self._secret = kwargs["secret"]
            del kwargs["secret"]
        else:
            self._secret = None
        super().__init__(*args, **kwargs)

    @morepath.reify
    def secret(self):
        if self._secret:
            return self._secret
        return uuid4().hex

    def identify(self, request):
        identity = super().identify(request)
        if identity:

            @request.after
            def update_expiry(response):
                response.headers.add("Access-Control-Expose-Headers", "Authorization")
                request.app.remember_identity(response, request, identity)

            identity = Identity(request=request, userid=identity.userid)

        return identity


class IdentityPolicy(morepath.IdentityPolicy):
    def __init__(
        self,
        jwt_settings,
        itsdangerous_settings,
        api_root="/api",
        development_mode=False,
    ):
        self.api_root = api_root
        self.jwtpolicy = JWTWithAPIKeyIdentityPolicy(**jwt_settings)
        self.itsdangerouspolicy = ItsDangerousIdentityPolicy(**itsdangerous_settings)
        self.development_mode = development_mode

    def getpolicy(self, request):
        if self.development_mode and request.cookies.get("userid"):
            # allow cookie authentication on API in development mode
            return self.itsdangerouspolicy
        if request.path.startswith(self.api_root):
            return self.jwtpolicy
        return self.itsdangerouspolicy

    def identify(self, request: morepath.Request):
        policy = self.getpolicy(request)
        return policy.identify(request)

    def remember(self, response, request, identity):
        policy = self.getpolicy(request)
        return policy.remember(response, request, identity)

    def forget(self, response, request):
        policy = self.getpolicy(request)
        return policy.forget(response, request)
