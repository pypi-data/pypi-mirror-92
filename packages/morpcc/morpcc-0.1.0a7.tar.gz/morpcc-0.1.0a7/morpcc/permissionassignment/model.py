import morpfw
from .schema import PermissionAssignmentSchema
# 
from .modelui import PermissionAssignmentModelUI, PermissionAssignmentCollectionUI
# 

class PermissionAssignmentModel(morpfw.Model):
    schema = PermissionAssignmentSchema

# 
    def ui(self):
        return PermissionAssignmentModelUI(self.request, self,
                self.collection.ui())
# 


class PermissionAssignmentCollection(morpfw.Collection):
    schema = PermissionAssignmentSchema

# 
    def ui(self):
        return PermissionAssignmentCollectionUI(self.request, self)
# 

