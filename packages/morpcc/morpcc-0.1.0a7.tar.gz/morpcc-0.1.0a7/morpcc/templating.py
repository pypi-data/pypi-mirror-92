import functools
import json
import os
from importlib import import_module

from pkg_resources import resource_filename

import morepath
import morpfw
from deform import Form
from morepath.publish import resolve_model

from .app import App
from .root import Root
from .util import permits


@App.template_render(extension=".pt")
def get_chameleon_render(loader, name, original_render):

    template = loader.load(name, "xml")

    def render(content, request: morepath.Request):

        main_template = loader.load("master/main_template.pt", "xml")
        load_template = functools.partial(loader.load, format="xml")
        context = request.resolve_path()

        def _permits(permission, request=request, context=context):
            if isinstance(context, str):
                context = request.resolve_path(context)
            return permits(request, context, permission)

        variables = {
            "request": request,
            "context": context,
            "main_template": main_template,
            "app": request.app,
            "permits": _permits,
            "settings": request.app.settings,
            "json": json,
            "load_template": load_template,
        }
        variables.update(content or {})
        return original_render(template.render(**variables), request)

    return render


@App.template_directory()
def get_template_directory():
    return "templates"


def set_deform_override():
    deform_templates = resource_filename("deform", "templates")
    form_templates = resource_filename("morpcc", os.path.join("templates", "deform"))
    search_path = (form_templates, deform_templates)
    Form.set_zpt_renderer(search_path)


set_deform_override()
