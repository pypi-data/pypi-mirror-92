import logging
import traceback
import urllib.parse

import morepath
import morpfw
from morepath.authentication import NO_IDENTITY
from morpfw.authn.pas.exc import UserDoesNotExistsError
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers.python import PythonTracebackLexer
from webob.exc import (
    HTTPForbidden,
    HTTPInternalServerError,
    HTTPNotFound,
    HTTPUnauthorized,
)

from ..app import App
from ..root import Root

logger = logging.getLogger("morpcc")


@App.view(model=HTTPNotFound)
def httpnotfound_error(context, request: morepath.Request):
    @request.after
    def adjust_status(response):
        response.status = 404

    if request.path.startswith("/api/"):
        return morepath.render_json(
            {"status": "error", "message": "Object Not Found : %s" % request.path},
            request,
        )
    else:
        render = request.app.config.template_engine_registry.get_template_render(
            "master/error_404.pt", morepath.render_html
        )
        return render({}, request)


@App.view(model=HTTPForbidden)
def forbidden_error(context, request):
    @request.after
    def nocache(response):
        response.headers.add("Cache-Control", "no-store")

    if request.identity is NO_IDENTITY and not request.path.startswith("/api/"):

        @request.after
        def forget(response):
            request.app.forget_identity(response, request)

        return morepath.redirect(
            request.relative_url(
                "/login?came_from=%s" % urllib.parse.quote(request.url)
            )
        )

    @request.after
    def adjust_status(response):
        response.status = 403

    #   FIXME: should log this when a config for DEBUG_SECURITY is enabled
    #    logger.error(traceback.format_exc())
    if request.path.startswith("/api/"):
        return morepath.render_json(
            {"status": "error", "message": "Access Denied : %s" % request.path}, request
        )
    else:
        render = request.app.config.template_engine_registry.get_template_render(
            "master/error_403.pt", morepath.render_html
        )
        return render({}, request)


@App.view(model=Exception)
def internalserver_error(context, request):
    @request.after
    def adjust_status(response):
        response.status = 500

    tb = traceback.format_exc()
    logger.error("Internal Server Error\n" + tb)

    if request.path.startswith("/api/"):
        return morepath.render_json(
            {
                "status": "error",
                "message": "Internal server error",
                "traceback": tb.split("\n"),
            },
            request,
        )
    else:
        render = request.app.config.template_engine_registry.get_template_render(
            "master/error_500.pt", morepath.render_html
        )
        formatter = HtmlFormatter()
        highlighted = highlight(tb, PythonTracebackLexer(), formatter)
        return render({"traceback": highlighted}, request)


@App.view(model=HTTPUnauthorized)
def unauthorized_error(context, request):
    @request.after
    def nocache(response):
        request.app.forget_identity(response, request)
        response.headers.add("Cache-Control", "no-store")

    return morepath.redirect(
        request.relative_url("/login?came_from=%s" % urllib.parse.quote(request.url))
    )


@App.view(model=UserDoesNotExistsError)
def unauthorized_nouser_error(context, request):
    @request.after
    def nocache(response):
        request.app.forget_identity(response, request)
        response.headers.add("Cache-Control", "no-store")

    return morepath.redirect(
        request.relative_url("/login?came_from=%s" % urllib.parse.quote(request.url))
    )
