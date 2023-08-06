import morpfw
from .schema import ObjectPermissionAssignmentSchema
# 
from .modelui import ObjectPermissionAssignmentModelUI, ObjectPermissionAssignmentCollectionUI
# 

class ObjectPermissionAssignmentModel(morpfw.Model):
    schema = ObjectPermissionAssignmentSchema

# 
    def ui(self):
        return ObjectPermissionAssignmentModelUI(self.request, self,
                self.collection.ui())
# 


class ObjectPermissionAssignmentCollection(morpfw.Collection):
    schema = ObjectPermissionAssignmentSchema

# 
    def ui(self):
        return ObjectPermissionAssignmentCollectionUI(self.request, self)
# 

