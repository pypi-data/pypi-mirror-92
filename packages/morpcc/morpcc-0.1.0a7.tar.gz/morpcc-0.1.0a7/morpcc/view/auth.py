import html
import urllib.parse
from dataclasses import dataclass, field

import deform
import morepath
from inverter import dc2colander
from morpfw.authn.pas import permission as authperm
from morpfw.authn.pas.user.path import get_user_collection
from webob.exc import HTTPNotFound

from ..app import App
from ..root import Root


@dataclass
class LoginForm(object):

    username: str = field(metadata={"required": True})
    password: str = field(
        metadata={"required": True, "deform.widget": deform.widget.PasswordWidget()}
    )


@App.html(model=Root, name="login", template="master/anon-form.pt")
def login(context, request):
    schema = request.app.get_schemaextender(LoginForm)
    formschema = dc2colander.convert(
        schema, request=request, default_tzinfo=request.timezone()
    )
    fs = formschema()
    fs = fs.bind(context=context, request=request)
    buttons = ["Login"]
    if request.app.get_config("morpfw.new_registration.enabled", True):
        buttons.append(
            deform.Button(
                "register",
                title="Register",
                type="link",
                value=request.relative_url("/register"),
            )
        )
    return {
        "form_title": "Login",
        "form": deform.Form(fs, buttons=buttons),
    }


@App.html(
    model=Root, name="login", template="master/anon-form.pt", request_method="POST"
)
def process_login(context, request):
    controls = list(request.POST.items())
    schema = request.app.get_schemaextender(LoginForm)
    formschema = dc2colander.convert(
        schema, request=request, default_tzinfo=request.timezone()
    )
    fs = formschema()
    fs = fs.bind(context=context, request=request)
    form = deform.Form(fs)
    failed = False
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True

    if not failed:
        username = data["username"].lower()
        password = data["password"]
        collection = request.get_collection("morpfw.pas.user")

        if not collection.authenticate(username, password):
            request.notify(
                "error", "Invalid Login", "Please check your username / password"
            )
            return morepath.redirect(request.relative_url("/login"))

        @request.after
        def remember(response):
            """Remember the identity of the user logged in."""
            # We pass the extra info to the identity object.
            response.headers.add("Access-Control-Expose-Headers", "Authorization")
            u = collection.get_by_username(username)
            identity = morepath.Identity(u.userid)
            request.app.remember_identity(response, request, identity)

        came_from = request.GET.get("came_from", "")
        if came_from:
            came_from = urllib.parse.unquote(came_from)
        else:
            came_from = request.relative_url("/")
        return morepath.redirect(came_from)

    request.notify("error", "Invalid Login", "Please check your username / password")

    return morepath.redirect(request.relative_url("/login"))


@App.view(model=Root, name="logout")
def logout(context, request):
    @request.after
    def forget(response):
        request.app.forget_identity(response, request)

    return morepath.redirect(request.relative_url("/"))


@dataclass
class RegistrationForm(object):
    username: str = field(metadata={"required": True})
    email: str = field(metadata={"required": True})
    password: str = field(
        metadata={"required": True, "deform.widget": deform.widget.PasswordWidget(),}
    )
    password_validate: str = field(
        metadata={"required": True, "deform.widget": deform.widget.PasswordWidget(),}
    )


@App.html(
    model=Root, name="register", template="master/anon-form.pt",
)
def register(context, request):
    enabled = request.app.get_config("morpfw.new_registration.enabled", True)
    if not enabled:
        raise HTTPNotFound()
    schema = request.app.get_schemaextender(RegistrationForm)
    formschema = dc2colander.convert(
        schema, request=request, default_tzinfo=request.timezone()
    )
    fs = formschema()
    fs = fs.bind(context=context, request=request)
    return {
        "form_title": "Register",
        "form": deform.Form(
            fs,
            buttons=(
                "Register",
                deform.Button(
                    "login",
                    title="Login",
                    type="link",
                    value=request.relative_url("/login"),
                ),
            ),
        ),
    }


@App.view(model=Root, name="register", request_method="POST")
def process_register(context, request):
    enabled = request.app.get_config("morpfw.new_registration.enabled", True)
    if not enabled:
        raise HTTPNotFound()
    controls = list(request.POST.items())
    schema = request.app.get_schemaextender(RegistrationForm)
    formschema = dc2colander.convert(
        schema, request=request, default_tzinfo=request.timezone()
    )
    fs = formschema()
    fs = fs.bind(context=context, request=request)
    form = deform.Form(fs)
    failed = False
    try:
        data = form.validate(controls)
    except deform.ValidationFailure as e:
        form = e
        failed = True

    if not failed:
        collection = get_user_collection(request)
        if data["password"] != data["password_validate"]:
            request.notify(
                "error", "Password does not match", "Please check your password"
            )
            return morepath.redirect(request.relative_url("/register"))

        username = data["username"].lower()
        email = data["email"]
        if collection.get_by_username(username):
            request.notify(
                "error", "Username already taken", "Please use a different username"
            )
            return morepath.redirect(request.relative_url("/register"))

        if collection.get_by_email(email):
            request.notify(
                "error",
                "Email already registered",
                "Log-in using your existing account",
            )
            return morepath.redirect(request.relative_url("/register"))

        del data["password_validate"]
        data["username"] = data["username"].lower()
        user = collection.create(data)

        @request.after
        def remember(response):
            """Remember the identity of the user logged in."""
            # We pass the extra info to the identity object.
            response.headers.add("Access-Control-Expose-Headers", "Authorization")
            identity = morepath.Identity(user.userid)
            request.app.remember_identity(response, request, identity)

        return morepath.redirect(request.relative_url("/"))
