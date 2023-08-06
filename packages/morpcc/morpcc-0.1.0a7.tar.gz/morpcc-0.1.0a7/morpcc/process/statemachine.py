from datetime import datetime

import pytz

import morpfw

from ..app import App
from .model import ProcessModel


class ProcessStateMachine(morpfw.StateMachine):

    states = ["new", "running", "cancelled", "failed", "success"]
    transitions = [
        {"trigger": "start", "source": "new", "dest": "running"},
        {"trigger": "cancel", "source": ["running", "new"], "dest": "cancelled"},
        {"trigger": "fail", "source": ["running", "new"], "dest": "failed"},
        {"trigger": "complete", "source": "running", "dest": "success"},
    ]

    protected_transitions = ["fail", "complete"]

    def on_enter_running(self):
        context = self._context
        context.update({"start": datetime.now(tz=pytz.UTC)}, deserialize=False)

    def on_exit_running(self):
        context = self._context
        context.update({"end": datetime.now(tz=pytz.UTC)}, deserialize=False)

    def on_enter_cancelled(self):
        context = self._context
        request = self._request
        request.app.celery.control.revoke(context["task_id"], terminate=True)


@App.statemachine(model=ProcessModel)
def get_statemachine(context):
    return ProcessStateMachine(context)
