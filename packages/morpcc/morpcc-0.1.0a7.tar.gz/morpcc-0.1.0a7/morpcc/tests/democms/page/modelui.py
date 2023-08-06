from morpcc.crud.model import ModelUI, CollectionUI


class PageModelUI(ModelUI):
    pass


class PageCollectionUI(CollectionUI):
    modelui_class = PageModelUI

    columns = [
        {'title': 'Title', 'name': 'title'},
        {'title': 'Created On', 'name': 'created'},
        {'title': 'Last Modified', 'name': 'modified'},
        {'title': 'Actions', 'name': 'structure:buttons'}
    ]
