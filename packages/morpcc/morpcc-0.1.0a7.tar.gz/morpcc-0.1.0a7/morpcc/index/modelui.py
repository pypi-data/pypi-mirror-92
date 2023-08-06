from morpcc.crud.model import CollectionUI, ModelUI


class IndexModelUI(ModelUI):
    pass


class IndexCollectionUI(CollectionUI):
    modelui_class = IndexModelUI


class IndexContentModelUI(ModelUI):
    pass


class IndexContentCollectionUI(CollectionUI):
    modelui_class = IndexContentModelUI

    @property
    def columns(self):
        columns = []

        for n, attr in self.collection.__parent__.attributes().items():
            columns.append({"title": attr["title"], "name": n})
        columns.append({"title": "Actions", "name": "structure:buttons"})

        return columns
