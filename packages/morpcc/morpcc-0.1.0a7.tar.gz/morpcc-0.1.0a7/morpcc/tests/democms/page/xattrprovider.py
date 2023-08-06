from ..app import App
from .model import PageModel
from morpfw.crud.xattrprovider.fieldxattrprovider import FieldXattrProvider
from dataclasses import dataclass
from typing import Optional


@dataclass
class PageXattrSchema(object):

    attribute1: Optional[str] = None
    attribute2: Optional[int] = None


class PageXattrProvider(FieldXattrProvider):

    schema = PageXattrSchema


@App.xattrprovider(model=PageModel)
def get_xattrprovider(context):
    return PageXattrProvider(context)
