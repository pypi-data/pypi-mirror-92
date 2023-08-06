import html

import colander
import deform
import morpfw
from inverter import dc2colander


class ModelUI(object):

    view_include_fields: list = []
    view_exclude_fields: list = [
        "id",
        "uuid",
        "creator",
        "created",
        "modified",
        "state",
        "deleted",
        "xattrs",
        "blobs",
    ]
    edit_include_fields: list = []
    edit_exclude_fields: list = [
        "id",
        "uuid",
        "creator",
        "created",
        "modified",
        "state",
        "deleted",
        "xattrs",
        "blobs",
    ]

    default_view = "view"

    @property
    def update_view_enabled(self):
        return self.model.update_view_enabled

    @property
    def delete_view_enabled(self):
        return self.model.delete_view_enabled

    @property
    def identifier(self):
        return self.model.identifier

    @property
    def uuid(self):
        return self.model.uuid

    @property
    def schema(self):
        return self.model.schema

    def __init__(self, request, model, collection_ui):
        self.request = request
        self.model = model
        self.collection_ui = collection_ui

    def transitions(self):
        sm = self.model.statemachine()
        if sm:
            return list(
                [
                    i
                    for i in sm._machine.get_triggers(sm.state)
                    if not i.startswith("to_")
                ]
            )
        return []

    def __getitem__(self, key):
        return self.model[key]

    def __setitem__(self, key, value):
        self.model[key] = value

    def __delitem__(self, key):
        del self.model[key]


class CollectionUI(object):

    modelui_class = ModelUI

    create_include_fields: list = []
    create_exclude_fields: list = [
        "id",
        "uuid",
        "creator",
        "created",
        "modified",
        "state",
        "deleted",
        "xattrs",
        "blobs",
    ]

    default_view = "listing"

    @property
    def create_view_enabled(self):
        return self.collection.create_view_enabled

    @property
    def page_title(self):
        try:
            typeinfo = self.request.app.get_typeinfo_by_schema(
                schema=self.collection.schema, request=self.request
            )
            return typeinfo["title"]
        except KeyError:
            pass
        return str(self.collection.__class__.__name__)

    @property
    def listing_title(self):
        return "Contents"

    @property
    def columns(self):
        columns = []
        if "created" in self.collection.schema.__dataclass_fields__.keys():
            n = "created"
            field = morpfw.Schema.__dataclass_fields__["created"]
            default_title = n.replace("_", " ").title()
            title = field.metadata.get("title", default_title)
            columns.append({"title": title, "name": n})

        for n, field in self.collection.schema.__dataclass_fields__.items():
            if n in morpfw.Schema.__dataclass_fields__.keys():
                continue
            default_title = n.replace("_", " ").title()
            title = field.metadata.get("title", default_title)
            columns.append({"title": title, "name": n})

        columns.append({"title": "Actions", "name": "structure:buttons"})
        return columns

    @property
    def columns_order(self):
        return [[0, "desc"]]

    def __init__(self, request, collection):
        self.request = request
        self.collection = collection

    def get_structure_column(self, obj, request, column_type):
        column_type = column_type.replace("structure:", "")
        coldata = request.app.get_structure_column(
            model=obj, request=request, name=column_type
        )
        return coldata

    def search(self, query=None, offset=0, limit=None, order_by=None, secure=False):
        objs = self.collection.search(query, offset, limit, order_by, secure)
        return list([self.modelui_class(self.request, o, self) for o in objs])

    def get(self, identifier):
        obj = self.collection.get(identifier)
        if obj:
            return self.modelui_class(self.request, obj, self)
        return None

    def render_column(self, record, name):
        if getattr(self, "_render_column", None) is None:
            formschema = dc2colander.convert(
                self.collection.schema,
                request=self.request,
                default_tzinfo=self.request.timezone(),
            )

            def render_column(rec, colname):
                fs = formschema()
                fs = fs.bind(context=rec, request=self.request)
                form = deform.Form(fs)
                field = form[colname]
                value = rec[colname]
                if value is None:
                    value = colander.null
                return field.render(
                    value, readonly=True, request=self.request, context=rec
                )

            self._render_column = render_column
        return self._render_column(record, name)
