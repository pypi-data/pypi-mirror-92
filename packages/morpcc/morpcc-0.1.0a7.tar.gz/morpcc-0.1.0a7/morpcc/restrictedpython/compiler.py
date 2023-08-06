import logging

import six

from RestrictedPython import compile_restricted
from RestrictedPython import safe_builtins as orig_safe_builtins
from RestrictedPython import safe_globals as orig_safe_globals
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter
from RestrictedPython.Guards import (
    full_write_guard,
    guarded_iter_unpack_sequence,
    safer_getattr,
)
from RestrictedPython.PrintCollector import PrintCollector

log = logging.getLogger("morpcc.restrictedpython")


def default_inplacevar(op, x, y):
    if op == "+=":
        return x + y
    raise Exception("{} operator is not allowed".format(op))


if six.PY3:
    import_default_level = 0
else:
    import_default_level = -1


class RestrictedImportError(Exception):
    pass


class ImportGuard(object):
    def __init__(self, app):
        self.app = app

    def __call__(
        self, name, globals=None, locals=None, fromlist=None, level=import_default_level
    ):
        if self.app is None:
            raise RestrictedImportError("Access Denied")

        if fromlist is None:
            fromlist = ()
        if globals is None:
            globals = {}
        if locals is None:
            locals = {}

        if level != import_default_level:
            raise RestrictedImportError(
                "Using import with a level specification isn't supported: %s" % name
            )

        return self.app.get_restricted_module(name)


class Print(PrintCollector):
    def _call_print(self, *objects, **kwargs):
        log.info(" ".join(objects))


safe_builtins = orig_safe_builtins.copy()
safe_globals = orig_safe_globals.copy()
safe_globals["dir"] = dir
safe_globals["_getiter_"] = default_guarded_getiter
safe_globals["_getitem_"] = default_guarded_getitem
safe_globals["_iter_unpack_sequence_"] = guarded_iter_unpack_sequence
safe_globals["_write_"] = full_write_guard
safe_globals["_inplacevar_"] = default_inplacevar
safe_globals["__builtins__"] = safe_builtins
safe_globals["getattr"] = safer_getattr
safe_globals["enumerate"] = enumerate
safe_globals["log"] = log


def get_restricted_function(app, bytecode, name, local_vars=None):
    local_vars = local_vars or {}
    glob = safe_globals.copy()
    glob["__builtins__"]["__import__"] = ImportGuard(app)
    exec(bytecode, glob, local_vars)
    func = local_vars[name]
    del local_vars[name]
    func.__globals__.update(local_vars)
    return func
