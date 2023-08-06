import typing
from dataclasses import dataclass, field

import deform
import deform.widget
import rulez
from inverter import dc2colander
from morpcc.crud.view.edit import edit as default_edit
from morpcc.crud.view.listing import listing as default_listing
from morpcc.crud.view.view import view as default_view
from morpfw import permission, request
from morpfw.crud import permission as crudperm
from morpfw.crud.batching import CollectionBatching
from morpfw.crud.permission import Search

from ..app import App
from .model import ProcessCollection, ProcessModel

#
from .modelui import ProcessCollectionUI, ProcessModelUI
from .statemachine import ProcessStateMachine

#


def signal_widget_factory(request):
    col = request.get_collection("morpcc.process")
    vals = col.aggregate(
        group={"signal": "signal", "total": {"function": "count", "field": "id"}}
    )
    values = [("", "")] + list(sorted([(v["signal"], v["signal"]) for v in vals]))
    return deform.widget.SelectWidget(values=values)


def state_widget_factory(request):
    values = [("", "")] + list([(v, v) for v in ProcessStateMachine.states])
    return deform.widget.SelectWidget(values=values)


@dataclass
class SearchForm(object):

    signal: typing.Optional[str] = field(
        default=None, metadata={"deform.widget_factory": signal_widget_factory}
    )
    state: typing.Optional[str] = field(
        default=None, metadata={"deform.widget_factory": state_widget_factory}
    )


@App.html(
    model=ProcessCollectionUI,
    name="listing",
    permission=crudperm.Search,
    template="master/process/listing.pt",
)
def listing(context, request):
    page = int(request.GET.get("page", 0))
    query = None
    formschema = dc2colander.convert(SearchForm, request=request)()
    formschema = formschema.bind(request=request, context=context)
    form = deform.Form(formschema, buttons=("Submit",), method="GET")
    data = {}
    if "__formid__" in request.GET:
        controls = list(request.GET.items())
        failed = False
        try:
            data = form.validate(controls)
        except deform.ValidationFailure as e:
            form = e
            failed = True

        if not failed:
            signal = data["signal"]
            state = data["state"]
            if signal:
                query = rulez.field["signal"] == signal
            if state:
                if query is None:
                    query = rulez.field["state"] == state
                else:
                    query = rulez.and_(query, rulez.field["state"] == state)
    batch = CollectionBatching(
        request, context.collection, query=query, pagesize=5, pagenumber=page
    )
    return {
        "batch": batch,
        "search_form": form,
        "search_data": data,
    }
