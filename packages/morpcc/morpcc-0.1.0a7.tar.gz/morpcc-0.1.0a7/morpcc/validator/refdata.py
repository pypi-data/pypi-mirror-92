import re

import rulez


class ReferenceDataValidator(object):
    def __init__(self, referencedata_name, referencedata_property):
        self.referencedata_name = referencedata_name
        self.referencedata_property = referencedata_property

    def __call__(self, request, schema, field, value, mode=None):
        resource = self.get_resource(request, value)
        if not resource:
            return "Value does not exists in reference data : {}".format(value)

    def get_resource(self, request, identifier):
        col = request.get_collection("morpcc.referencedata")
        refdatas = col.search(rulez.field["name"] == self.referencedata_name)
        if not refdatas:
            return None
        refdata = refdatas[0]

        keycol = request.get_collection("morpcc.referencedatakey")
        keys = keycol.search(
            rulez.and_(
                rulez.field["referencedata_uuid"] == refdata.uuid,
                rulez.field["name"] == identifier,
            )
        )
        if not keys:
            return None
        return keys[0]
