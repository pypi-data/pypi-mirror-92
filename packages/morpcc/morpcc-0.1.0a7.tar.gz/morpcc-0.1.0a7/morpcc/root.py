import html

from morpfw.crud import permission as crudperms

from .app import App
from .permission import ViewHome
from .util import permits, typeinfo_link, types_navigation


class Root(object):
    def __init__(self, request):
        self.request = request


@App.path(model=Root, path="/")
def get_root(request):
    return Root(request)


@App.html(model=Root, permission=ViewHome, template="master/index.pt")
def index(context, request):
    return {
        "page_title": "Collections",
        "typeinfos": types_navigation(request),
    }
