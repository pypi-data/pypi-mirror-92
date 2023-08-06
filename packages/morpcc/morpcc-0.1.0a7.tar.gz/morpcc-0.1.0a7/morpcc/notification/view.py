from datetime import datetime

import morepath
import pytz
import timeago
from morpfw.crud import permission as crudperms
from morpfw.crud.batching import CollectionBatching

from ..app import App
from ..crud.view.view import view as default_view
from .modelui import NotificationCollectionUI, NotificationModelUI


@App.html(
    model=NotificationModelUI,
    name="view",
    template="master/crud/view.pt",
    permission=crudperms.View,
)
def view(context, request):
    if not context["read"]:
        context.model.update(
            {"read": datetime.now(tz=request.timezone())}, deserialize=False
        )

    linkmeta = context["link"]
    if linkmeta and "type" in linkmeta:
        try:
            link = request.resolve_metalink(linkmeta)
        except NotImplementedError:
            link = None
    else:
        link = None
    if not link:
        referer = request.headers.get("Referer")
        if referer:
            return morepath.redirect(referer)
    else:
        return morepath.redirect(link)

    return morepath.redirect(request.relative_url("/"))


@App.html(
    model=NotificationCollectionUI,
    name="listing",
    template="master/notification/listing.pt",
    permission=crudperms.View,
)
def listing(context, request):
    batch = CollectionBatching(
        request, context.collection, pagenumber=request.GET.get("page", 0)
    )
    now = datetime.now(tz=request.timezone())

    def get_icon_url(txt):
        if not txt:
            return None
        if txt.lower().startswith("http"):
            return txt
        elif txt.startswith("/"):
            return request.relative_url(txt)
        return None

    def _timeago(dt):
        return timeago.format(dt, now)

    return {"batch": batch, "get_icon_url": get_icon_url, "timeago": _timeago}

