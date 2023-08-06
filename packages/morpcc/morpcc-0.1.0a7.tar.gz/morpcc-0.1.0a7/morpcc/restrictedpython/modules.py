import datetime
import time

from ..app import App


@App.restricted_module("datetime")
def get_datetime(name):
    return datetime


@App.restricted_module("time")
def get_time(name):
    return time
