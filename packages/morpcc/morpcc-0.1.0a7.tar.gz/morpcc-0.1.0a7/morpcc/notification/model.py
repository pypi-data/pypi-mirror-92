import typing

import morpfw
import rulez

from .modelui import NotificationCollectionUI, NotificationModelUI
from .schema import NotificationSchema


class NotificationModel(morpfw.Model):
    schema = NotificationSchema

    def ui(self):
        return NotificationModelUI(self.request, self, self.collection.ui())

    def title(self):
        return self["subject"]


CURRENT_USER = object()


class NotificationCollection(morpfw.Collection):
    schema = NotificationSchema

    def ui(self):
        return NotificationCollectionUI(self.request, self)

    def search(self, query=None, *args, **kwargs):
        if kwargs.get("secure", True):
            if query:
                rulez.and_(rulez.field["userid"] == self.request.identity.userid, query)
            else:
                query = rulez.field["userid"] == self.request.identity.userid
        return super().search(query, *args, **kwargs)
