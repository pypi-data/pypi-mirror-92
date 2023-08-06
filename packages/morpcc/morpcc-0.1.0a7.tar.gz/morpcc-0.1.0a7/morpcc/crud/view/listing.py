import html
import json
import re
import typing
from dataclasses import field, make_dataclass

import colander
import deform
import morepath
import rulez
from boolean.boolean import ParseError
from inverter import dc2colander
from morpfw.crud import permission as crudperms

from ...app import App
from ...permission import ViewHome
from ..model import CollectionUI, ModelUI


@App.html(
    model=CollectionUI,
    name="listing",
    template="master/crud/listing.pt",
    permission=crudperms.Search,
)
def listing(context, request):
    column_options = []
    columns = []
    order = context.columns_order

    for c in context.columns:
        columns.append(c["title"])
        sortable = True
        if c["name"].startswith("structure:"):
            sortable = False
        column_options.append({"name": c["name"], "orderable": sortable})

    query_request_method = "GET"
    if len(context.columns) > 7:
        query_request_method = "POST"

    search_attrs = []
    for attrname, attr in context.collection.schema.__dataclass_fields__.items():
        searchable = attr.metadata.get("searchable", None)
        if searchable:
            metadata = {"required": False}
            for mf in [
                "title",
                "description",
                "deform.widget",
                "deform.widget_factory",
            ]:
                mvalue = attr.metadata.get(mf, None)
                if mvalue:
                    metadata[mf] = mvalue
            search_attrs.append(
                (attrname, attr.type, field(default=None, metadata=metadata))
            )

    if search_attrs:
        dc = make_dataclass("Form", search_attrs)
        formschema = dc2colander.convert(
            dc, request=request, default_tzinfo=request.timezone()
        )
        search_form = deform.Form(formschema(), buttons=("Search",))
    else:
        search_form = None

    data = _parse_dtdata(list(request.GET.items()))
    search_data = data["mfw_search"]

    return {
        "page_title": context.page_title,
        "listing_title": context.listing_title,
        "search_form": search_form,
        "search_data": search_data,
        "columns": columns,
        "column_options": json.dumps(column_options),
        "order": json.dumps(order),
        "datatable_method": query_request_method,
    }


column_pattern = re.compile(r"^columns\[(\d+)\]\[(\w+)\]$")
search_column_pattern = re.compile(r"^columns\[(\d+)\]\[(\w+)\]\[(\w+)\]$")
search_pattern = re.compile(r"^search\[(\w+)\]$")
mfw_search_pattern = re.compile(r"^mfw_search\[(\w+)\]$")
order_pattern = re.compile(r"order\[(\d+)\]\[(\w+)\]")


def _parse_dtdata(data):
    result = {}

    result["columns"] = []
    result["search"] = {}
    result["order"] = {}
    result["length"] = None
    result["start"] = 0
    result["draw"] = 1
    result["filter"] = None
    result["mfw_search"] = {}

    columns = [(k, v) for k, v in data if k.startswith("columns")]
    orders = [(k, v) for k, v in data if k.startswith("order")]
    mfilter = [(k, v) for k, v in data if k == "filter"]
    mfilter = mfilter[0][1] if mfilter else None

    column_data = {}
    for k, v in columns:
        m1 = column_pattern.match(k)
        m2 = search_column_pattern.match(k)
        if m1:
            i, o = m1.groups()
            column_data.setdefault(int(i), {})
            column_data[int(i)][o] = v
        elif m2:
            i, o, s = m2.groups()
            column_data.setdefault(int(i), {})
            column_data[int(i)].setdefault(o, {})
            column_data[int(i)][o][s] = v

    result["columns"] = []
    for k in sorted(column_data.keys()):
        result["columns"].append(column_data[k])

    order_data = {}
    for k, v in orders:
        i, o = order_pattern.match(k).groups()
        order_data.setdefault(int(i), {})
        if o == "column":
            order_data[int(i)][o] = int(v)
        else:
            order_data[int(i)][o] = v

    result["order"] = []
    for k in sorted(order_data.keys()):
        result["order"].append(order_data[k])

    in_sequence = False
    current_mfw_search = None
    for k, v in data:
        if in_sequence:
            i = mfw_search_pattern.match(k).groups()[0]
            if i == "__end__":
                in_sequence = False
                current_mfw_search = None
                continue
            result["mfw_search"][current_mfw_search].append(v)
            continue

        if k == "draw":
            result["draw"] = int(v)
        elif k == "_":
            result["_"] = v
        elif k == "start":
            result["start"] = int(v)
        elif k == "length":
            result["length"] = int(v)
        elif k.startswith("search"):
            i = search_pattern.match(k).groups()[0]
            result["search"].setdefault(i, {})
            result["search"][i] = v
        elif k.startswith("mfw_search"):
            i = mfw_search_pattern.match(k).groups()[0]
            if i == "__start__":
                current_mfw_search, typ = v.split(":")
                in_sequence = True
                result["mfw_search"].setdefault(current_mfw_search, [])
                continue
            result["mfw_search"][i] = v

    if mfilter:
        result["filter"] = rulez.parse_dsl(mfilter)

    return result


def _dt_result_render(context, request, columns, objs):
    rows = []
    collection = context.collection
    formschema = dc2colander.convert(
        collection.schema, request=request, default_tzinfo=request.timezone()
    )
    for o in objs:
        row = []
        fs = formschema()
        fs = fs.bind(context=o, request=request)
        form = deform.Form(fs)
        for c in columns:
            if c["name"].startswith("structure:"):
                row.append(context.get_structure_column(o, request, c["name"]))
            else:
                field = form[c["name"]]
                value = o.data[c["name"]]
                if value is None:
                    value = colander.null
                row.append(
                    field.render(value, readonly=True, request=request, context=o)
                )
        rows.append(row)
    return rows


def datatable_search(
    context,
    request,
    additional_filters=None,
    renderer=_dt_result_render,
    request_method="GET",
):
    collection = context.collection
    data = list(getattr(request, request_method).items())
    data = _parse_dtdata(data)
    # Data coming in explicitly from GET
    qs_data = list(request.GET.items())
    qs_data = _parse_dtdata(qs_data)
    if "mfw_search" in qs_data:
        data["mfw_search"] = qs_data["mfw_search"]
    search = []
    if data["search"] and data["search"]["value"]:
        for fn, field in context.collection.schema.__dataclass_fields__.items():
            if field.metadata.get("format", None) == "uuid":
                continue
            if field.type == str:
                search.append(
                    {"field": fn, "operator": "~", "value": data["search"]["value"]}
                )
            elif field.type.__origin__ == typing.Union:
                if str in field.type.__args__:
                    search.append(
                        {"field": fn, "operator": "~", "value": data["search"]["value"]}
                    )

    if data["mfw_search"]:
        mfw_search = []
        for sfn, value in data["mfw_search"].items():
            value = (value or "").strip()
            if not value:
                continue

            if sfn not in context.collection.schema.__dataclass_fields__:
                continue

            field = context.collection.schema.__dataclass_fields__[sfn]
            if field.metadata.get("format", None) == "uuid":
                mfw_search.append({"field": sfn, "operator": "==", "value": value})
            elif field.type == str:
                mfw_search.append({"field": sfn, "operator": "~", "value": value})
            elif field.type == bool:
                val = True if value.lower() == "true" else False
                mfw_search.append({"field": sfn, "operator": "==", "value": val})
            elif field.type.__origin__ == typing.Union:
                if str in field.type.__args__:
                    mfw_search.append({"field": sfn, "operator": "~", "value": value})
                elif bool in field.type.__args__:
                    val = True if value.lower() == "true" else False
                    mfw_search.append({"field": sfn, "operator": "==", "value": val})
        search.append(rulez.and_(*mfw_search))
    if search:
        if len(search) > 1:
            search = rulez.or_(*search)
        else:
            search = search[0]
    else:
        search = None
    if data["filter"]:
        if search:
            search = rulez.and_(data["filter"], search)
        else:
            search = data["filter"]

    if additional_filters:
        if search:
            search = rulez.and_(additional_filters, search)
        else:
            search = additional_filters

    order_by = None
    if data["order"]:
        colidx = data["order"][0]["column"]
        order_col = data["columns"][colidx]["name"]
        order_col_orderable = data["columns"][colidx].get("orderable", "true")
        if order_col_orderable in ["true"]:
            order_col_orderable = True
        elif order_col_orderable in ["false"]:
            order_col_orderable = False
        else:
            order_col_orderable = True

        if not order_col_orderable:
            order_by = None
        elif order_col.startswith("structure:"):
            order_by = None
        else:
            order_by = (order_col, data["order"][0]["dir"])
    try:
        objs = collection.search(
            query=search, limit=data["length"], offset=data["start"], order_by=order_by,
        )
    except NotImplementedError:
        objs = collection.search(
            limit=data["length"], offset=data["start"], order_by=order_by
        )
    total = collection.aggregate(
        query=data["filter"], group={"count": {"function": "count", "field": "uuid"}}
    )
    try:
        total_filtered = collection.aggregate(
            query=search, group={"count": {"function": "count", "field": "uuid"}}
        )
    except NotImplementedError:
        total_filtered = total

    rows = renderer(context, request, data["columns"], objs)
    return {
        "draw": data["draw"],
        "recordsTotal": total[0]["count"],
        "recordsFiltered": total_filtered[0]["count"],
        "data": rows,
    }


@App.json(model=CollectionUI, name="datatable.json", permission=crudperms.Search)
def datatable(context, request):
    return datatable_search(context, request)


@App.json(
    model=CollectionUI,
    name="datatable.json",
    request_method="POST",
    permission=crudperms.Search,
)
def datatable(context, request):
    return datatable_search(context, request, request_method="POST")

