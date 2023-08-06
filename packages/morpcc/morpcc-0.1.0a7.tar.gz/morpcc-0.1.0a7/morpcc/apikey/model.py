from ..crud.model import CollectionUI, ModelUI


class APIKeyModelUI(ModelUI):

    edit_include_fields = ["name"]


class APIKeyCollectionUI(CollectionUI):

    modelui_class = APIKeyModelUI

    create_include_fields = ["name"]

    columns = [
        {"title": "Name", "name": "name"},
        {"title": "Identity", "name": "api_identity"},
        {"title": "Actions", "name": "structure:buttons"},
    ]
