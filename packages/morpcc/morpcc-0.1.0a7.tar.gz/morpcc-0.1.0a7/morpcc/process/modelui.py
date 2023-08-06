from morpcc.crud.model import ModelUI, CollectionUI


class ProcessModelUI(ModelUI):
    pass


class ProcessCollectionUI(CollectionUI):
    modelui_class = ProcessModelUI
