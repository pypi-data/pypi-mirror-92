import os
import shutil
import sys
import time
import traceback
import zipfile
from datetime import datetime

import pytz
import rulez
import transaction
from celery.app.task import Context
from celery.result import AsyncResult
from morpfw.signal.signal import (
    SCHEDULEDTASK_COMPLETED,
    SCHEDULEDTASK_FAILED,
    SCHEDULEDTASK_FINALIZED,
    SCHEDULEDTASK_STARTING,
    TASK_COMPLETED,
    TASK_FAILED,
    TASK_FINALIZED,
    TASK_STARTING,
    TASK_SUBMITTED,
)

from ..app import App


class TaskType(object):
    TRIGGERED_TASK = "triggered"
    SCHEDULED_TASK = "scheduled"


class OutputRouter(object):
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for stream in self.streams:
            stream.write(s)


class IOHandler(object):
    """
        Handle STDOUT and STDERR to log file. 
        NOTE: this doesn't work with multithreading
    """

    DEFAULT_WORKDIR = os.getcwd()
    DEFAULT_STDOUT = sys.stdout
    DEFAULT_STDERR = sys.stderr
    STDOUTS = {}
    STDERRS = {}

    def __init__(self, request, task_id):
        config = request.app.settings.configuration.__dict__
        self.task_id = task_id
        self.log_path = config.get("morpcc.worker.task_dir", "/tmp/")
        self.task_work_dir = os.path.join(
            os.path.abspath(self.log_path), "mfw-%s" % self.task_id
        )

    def redirect(self):

        if not os.path.exists(self.task_work_dir):
            os.makedirs(self.task_work_dir)

        os.chdir(self.task_work_dir)
        self._open()

    def restore(self):
        os.chdir(os.environ.get("MORP_WORKDIR", IOHandler.DEFAULT_WORKDIR))
        self._close()
        package = self.package_task()
        self.clear_task_dir()
        return package

    def package_task(self):
        filename = "/tmp/mfw-{}.zip".format(self.task_id)
        with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.task_work_dir):
                relpath = root.replace(self.task_work_dir, "./")
                for f in files:
                    print("packaging %s" % (os.path.join(root, f)))
                    zipf.write(os.path.join(root, f), arcname=os.path.join(relpath, f))
        return filename

    def clear_task_dir(self):
        shutil.rmtree(self.task_work_dir)

    def _open(self):
        stdout = open("stdout.log", "w")
        stderr = open("stderr.log", "w")
        IOHandler.STDOUTS[self.task_id] = stdout
        IOHandler.STDERRS[self.task_id] = stderr
        sys.stdout = OutputRouter(stdout, IOHandler.DEFAULT_STDOUT)
        sys.stderr = OutputRouter(stderr, IOHandler.DEFAULT_STDERR)

    def _close(self):
        if self.task_id in IOHandler.STDOUTS.keys():
            IOHandler.STDOUTS[self.task_id].close()
            del IOHandler.STDOUTS[self.task_id]

        if self.task_id in IOHandler.STDERRS.keys():
            IOHandler.STDERRS[self.task_id].close()
            del IOHandler.STDERRS[self.task_id]

        sys.stdout = IOHandler.DEFAULT_STDOUT
        sys.stderr = IOHandler.DEFAULT_STDERR


def handle_task_submitted(request, task_type, task_id, signal, params=None):

    col = request.get_collection("morpcc.process")
    res = col.search(rulez.field["task_id"] == task_id)
    if not res:
        obj = {"task_id": task_id, "signal": signal}
        if params:
            obj["params"] = params
        proc = col.create(obj, deserialize=False)
        print(
            "%s Task %s (%s) submitted"
            % (task_type.capitalize(), task_id, proc["signal"])
        )

        return proc


def handle_task_starting(request, task_type, task_id, signal=None):
    proc = None
    if task_type == TaskType.TRIGGERED_TASK:
        for retry in range(5):
            col = request.get_collection("morpcc.process")
            res = col.search(rulez.field["task_id"] == task_id)
            if res:
                proc = res[0]
                break
            print("Process Manager for Task %s is not ready" % task_id)
            time.sleep(5)
        if proc is None:
            print(
                "Unable to locate Process Manager for Task %s, "
                "proceeding without tracking" % task_id
            )
            return
    elif task_type == TaskType.SCHEDULED_TASK:
        proc = handle_task_submitted(request, task_type, task_id, signal)
    else:
        raise KeyError("Unknown task type")

    if proc:
        name = proc["signal"]
        sm = proc.statemachine()
        sm.start()
        transaction.commit()
        request.clear_db_session()
        transaction.begin()

        print("%s Task %s (%s) starting" % (task_type.capitalize(), name, task_id))
        IOHandler.DEFAULT_STDOUT = sys.stdout
        IOHandler.DEFAULT_STDERR = sys.stderr
        iohandler = IOHandler(request, task_id)
        iohandler.redirect()


def put_output(request, task_id, path):
    col = request.get_collection("morpcc.process")
    res = col.search(rulez.field["task_id"] == task_id)
    if res:
        proc = res[0]
        outf = open(path, "rb")
        proc.put_blob(
            field="output",
            filename="output.zip",
            mimetype="application/zip",
            fileobj=outf,
        )
        outf.close()
    if os.path.exists(path):
        os.unlink(path)


def handle_task_completed(request, task_type, task_id):
    col = request.get_collection("morpcc.process")
    res = col.search(rulez.field["task_id"] == task_id)
    if res:
        proc = res[0]
        name = proc["signal"]
        sm = proc.statemachine()
        sm.complete()
        transaction.commit()
        request.clear_db_session()
        transaction.begin()
        iohandler = IOHandler(request, task_id)
        output_package = iohandler.restore()
        put_output(request, task_id, output_package)
        print("%s Task %s (%s) completed" % (task_type.capitalize(), name, task_id))


def handle_task_failed(request, task_type, task_id):
    col = request.get_collection("morpcc.process")
    res = col.search(rulez.field["task_id"] == task_id)
    if res:
        proc = res[0]
        name = proc["signal"]
        sm = proc.statemachine()
        sm.fail()
        tb = traceback.format_exc()
        proc["traceback"] = tb
        transaction.commit()
        request.clear_db_session()
        transaction.begin()
        iohandler = IOHandler(request, task_id)
        output_package = iohandler.restore()
        put_output(request, task_id, output_package)
        print("%s Task %s (%s) failed" % (task_type.capitalize(), name, task_id))


@App.subscribe(model=AsyncResult, signal=TASK_SUBMITTED)
def task_submitted(app, request, context, signal):
    handle_task_submitted(
        request,
        TaskType.TRIGGERED_TASK,
        context.id,
        context.__signal__,
        context.__params__,
    )


@App.subscribe(model=Context, signal=TASK_STARTING)
def task_starting(app, request, context, signal):
    handle_task_starting(request, TaskType.TRIGGERED_TASK, context.id)


@App.subscribe(model=Context, signal=TASK_COMPLETED)
def task_completed(app, request, context, signal):
    handle_task_completed(request, TaskType.TRIGGERED_TASK, context.id)


@App.subscribe(model=Context, signal=TASK_FAILED)
def task_failed(app, request, context, signal):
    handle_task_failed(request, TaskType.TRIGGERED_TASK, context.id)


@App.subscribe(model=Context, signal=TASK_FINALIZED)
def task_finalized(app, request, context, signal):
    pass


@App.subscribe(model=Context, signal=SCHEDULEDTASK_STARTING)
def scheduled_task_starting(app, request, context, signal):
    handle_task_starting(
        request, TaskType.SCHEDULED_TASK, context.id, context.__job_name__
    )


@App.subscribe(model=Context, signal=SCHEDULEDTASK_COMPLETED)
def scheduled_task_completed(app, request, context, signal):
    handle_task_completed(request, TaskType.SCHEDULED_TASK, context.id)


@App.subscribe(model=Context, signal=SCHEDULEDTASK_FAILED)
def scheduled_task_failed(app, request, context, signal):
    handle_task_failed(request, TaskType.SCHEDULED_TASK, context.id)


@App.subscribe(model=Context, signal=SCHEDULEDTASK_FINALIZED)
def scheduled_task_finalized(app, request, context, signal):
    pass
