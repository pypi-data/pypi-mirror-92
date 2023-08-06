from morpfw.authn.pas.group.schema import GroupSchema

from ..crud.model import CollectionUI, ModelUI
from ..deform.referencewidget import ReferenceWidget

# GroupSchema.__dataclass_fields__["parent"].metadata["deform.widget"] = ReferenceWidget(
#    "morpfw.pas.group", "groupname", "groupname"
# )


class GroupModelUI(ModelUI):

    edit_include_fields = ["groupname"]


class GroupCollectionUI(CollectionUI):

    modelui_class = GroupModelUI

    create_include_fields = ["groupname"]

    columns = [
        {"title": "Group Name", "name": "groupname"},
        {"title": "Actions", "name": "structure:buttons"},
    ]
