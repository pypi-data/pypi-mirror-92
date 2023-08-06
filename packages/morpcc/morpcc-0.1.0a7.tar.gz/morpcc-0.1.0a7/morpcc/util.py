import copy
import dataclasses
from dataclasses import field
from datetime import date, datetime
from importlib import import_module

import colander
from deform.widget import HiddenWidget
from inverter.common import dataclass_check_type, dataclass_get_type
from morpfw.crud import permission as crudperms
from morpfw.interfaces import ISchema
from pkg_resources import resource_filename


def permits(request, context, permission):
    if isinstance(permission, str):
        perm_mod, perm_cls = permission.split(":")
        mod = import_module(perm_mod)
        klass = getattr(mod, perm_cls)
    else:
        klass = permission
    return request.app._permits(request.identity, context, klass)


def validate_form(request, obj, schema, form):
    form_data = obj.as_dict()
    validation_dict = obj.validation_dict()
    form_errors = []
    for attrname, attr in schema.__dataclass_fields__.items():
        field_errors = []
        field_value = form_data.get(attrname, None)

        metadata = attr.metadata
        if metadata.get("required", True):
            if form_data.get(attrname, None) is None:
                field_errors.append("Field is required")

        validators = metadata.get("validators", [])
        for validate in validators:
            error_msg = validate(request, schema, attr, field_value)
            if error_msg:
                field_errors.append(error_msg)

        if field_errors and attrname in form:
            field_error = colander.Invalid(form[attrname].widget, field_errors)
            form[attrname].widget.handle_error(form[attrname], field_error)

    for validate in schema.__validators__:
        error_msg = validate(request, schema, validation_dict)
        if error_msg:
            form_errors.append(error_msg)

    if form_errors:
        form_error = colander.Invalid(form.widget, form_errors)
        form.widget.handle_error(form, form_error)


def typeinfo_link(request, type_name):
    typeinfo = request.get_typeinfo(type_name)
    collection = typeinfo["collection_factory"](request)
    collectionui = collection.ui()
    return {
        "title": typeinfo["title"],
        "icon": typeinfo["icon"],
        "href": request.link(collectionui, "+{}".format(collectionui.default_view)),
    }


def types_navigation(request):
    types = request.app.config.type_registry.get_typeinfos(request)
    types_nav = []
    for typeinfo in types.values():
        if typeinfo.get("internal", False):
            continue
        collection = typeinfo["collection_factory"](request)
        collectionui = collection.ui()
        if permits(request, collectionui, crudperms.View):
            types_nav.append(typeinfo_link(request, typeinfo["name"]))

    types_nav.sort(key=lambda x: x["title"])
    return types_nav

