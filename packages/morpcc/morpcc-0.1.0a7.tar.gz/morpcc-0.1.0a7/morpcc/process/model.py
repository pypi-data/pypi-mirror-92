from datetime import date, datetime

import pytz

import morpfw
import rulez

#
from .modelui import ProcessCollectionUI, ProcessModelUI
from .schema import ProcessSchema

#


class ProcessModel(morpfw.Model):
    schema = ProcessSchema

    blob_fields = ["output"]
    #
    def ui(self):
        return ProcessModelUI(self.request, self, self.collection.ui())


#


class ProcessCollection(morpfw.Collection):
    schema = ProcessSchema

    #
    def ui(self):
        return ProcessCollectionUI(self.request, self)

    #

    def cleanup_running(self, age_hours=24):
        now = datetime.now(tz=pytz.UTC)
        for i in self.search(rulez.field["state"] == "running"):
            delta = i["start"] - now
            hours = (delta.days * 24) + int(delta.seconds / 60 / 60)
            if hours > age_hours:
                sm = i.statemachine()
                sm.cancel()

    def vacuum(self, age_days=30):
        now = datetime.now(tz=pytz.UTC)
        for i in self.search(rulez.field["state"] == "cancelled"):
            delta = i["start"] - now
            if delta.days > age_days:
                i.delete()
