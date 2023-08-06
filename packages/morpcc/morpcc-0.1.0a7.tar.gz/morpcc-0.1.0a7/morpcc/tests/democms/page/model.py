import morpfw

from .modelui import PageCollectionUI, PageModelUI
from .schema import PageSchema


class PageModel(morpfw.Model):
    schema = PageSchema

    blob_fields = ["attachment1", "attachment2"]

    def ui(self):
        return PageModelUI(self.request, self, self.collection.ui())


class PageCollection(morpfw.Collection):
    schema = PageSchema

    def ui(self):
        return PageCollectionUI(self.request, self)
