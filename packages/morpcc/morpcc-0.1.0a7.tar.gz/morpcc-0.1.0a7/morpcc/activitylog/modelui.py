from morpcc.crud.model import ModelUI, CollectionUI


class ActivityLogModelUI(ModelUI):
    pass


class ActivityLogCollectionUI(CollectionUI):
    modelui_class = ActivityLogModelUI
