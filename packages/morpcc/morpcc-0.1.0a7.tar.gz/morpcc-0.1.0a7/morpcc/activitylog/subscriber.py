from datetime import datetime

import morepath
from morpfw.crud import model, signals

from ..app import App
from .model import ActivityLogModel


@App.subscribe(signal=signals.OBJECT_CREATED, model=model.Model)
def log_create(app, request, obj, signal):
    log = request.get_collection("morpcc.activitylog")
    log.log(obj, "Created object")


@App.subscribe(signal=signals.OBJECT_UPDATED, model=model.Model)
def log_updated(app, request, obj, signal):
    log = request.get_collection("morpcc.activitylog")
    log.log(obj, "Modified object")


@App.subscribe(signal=signals.OBJECT_TOBEDELETED, model=model.Model)
def log_deleted(app, request, obj, signal):
    log = request.get_collection("morpcc.activitylog")
    log.log(obj, "Deleted object")
