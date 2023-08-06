import morepath
from morpfw.authn.pas.path import get_user_collection

from ..app import App

EXCLUDE_PREFIXES = ["/__static__/"]
EXCLUDE_PATHS = ["/logout", "/send-verification", "/verify"]


@App.tween_factory()
def make_tween(app, handler):
    verify_email = app.get_config("morpcc.registration_verify_email", False)
    if not verify_email:
        return handler

    def redirect_to_firstlogin(request: morepath.Request):
        for path in EXCLUDE_PREFIXES:
            if request.path.startswith(path):
                return handler(request)

        for path in EXCLUDE_PATHS:
            if request.path == path:
                return handler(request)

        userid = request.identity.userid
        if userid:
            col = get_user_collection(request)
            userobj = col.get_by_userid(userid)
            if userobj["state"] == "new" and not request.path.startswith("/firstlogin"):
                resp = morepath.redirect(request.relative_url("/firstlogin"))
                resp.headers["Cache-Control"] = "no-store"
                return resp
        return handler(request)

    return redirect_to_firstlogin
