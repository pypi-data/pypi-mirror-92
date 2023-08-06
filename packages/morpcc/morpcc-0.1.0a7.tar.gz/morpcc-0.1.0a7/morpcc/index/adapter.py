import json
import os
import pprint
import tempfile
import typing

import morpfw.crud.storage.sqlstorage
import rulez
import sqlalchemy
import sqlalchemy_jsonfield.jsonfield
import sqlalchemy_utils.types
from alembic import command
from alembic.autogenerate.api import (
    AutogenContext,
    compare_metadata,
    produce_migrations,
    render,
)
from alembic.autogenerate.compare import comparators
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.operations.ops import UpgradeOps
from inverter import dc2pgsqla
from RestrictedPython import compile_restricted, safe_globals
from sqlalchemy import MetaData, create_engine
from sqlalchemy.schema import CreateSchema

from .model import IndexCollection


def render_python_code(
    up_or_down_op,
    sqlalchemy_module_prefix="sa.",
    alembic_module_prefix="op.",
    render_as_batch=False,
    imports=(),
    render_item=None,
):
    """Render Python code given an :class:`.UpgradeOps` or
    :class:`.DowngradeOps` object.

    This is a convenience function that can be used to test the
    autogenerate output of a user-defined :class:`.MigrationScript` structure.

    """
    opts = {
        "sqlalchemy_module_prefix": sqlalchemy_module_prefix,
        "alembic_module_prefix": alembic_module_prefix,
        "user_module_prefix": None,
        "render_item": render_item,
        "render_as_batch": render_as_batch,
    }

    autogen_context = AutogenContext(None, opts=opts)
    autogen_context.imports = set(imports)
    return render._indent(render._render_cmd_body(up_or_down_op, autogen_context))


def _get_migrate_function(code):
    byte_code = compile_restricted(code, filename="<inline code>", mode="exec")
    glob = safe_globals.copy()
    glob.update(
        {
            "sa": sqlalchemy,
            "sqlalchemy_jsonfield": sqlalchemy_jsonfield,
            "morpfw": morpfw,
            "sqlalchemy_utils": sqlalchemy_utils,
        }
    )
    loc = {}
    exec(byte_code, glob, loc)
    return loc["migrate"]


class IndexDatabaseSyncAdapter(object):
    def __init__(self, context: IndexCollection, request):
        self.context = context
        self.request = request
        self.session = self.request.get_db_session("warehouse")
        self.engine = create_engine(self.session.bind.url)

        self.content_metadata = context.content_metadata()

        with self.engine.connect() as conn:
            # conn.dialect.default_schema_name = self.content_metadata.schema
            migration_context = MigrationContext.configure(
                conn, opts={"include_schemas": False}
            )
            self.upgrade_steps = self.get_upgrade_steps(migration_context)
            if len(self.upgrade_steps.ops):
                self.need_update = True
            else:
                self.need_update = False
            self.migration_code = self.get_migration_code()

    def get_upgrade_steps(self, migration_context) -> typing.List:
        content_metadata = self.context.content_metadata()
        content_metadata.clear()
        idx_dc = self.context.dataclass()
        tbl = dc2pgsqla.convert(idx_dc, content_metadata)
        upgrade_ops = UpgradeOps([])
        autogen_context = AutogenContext(migration_context, content_metadata)
        schemas = [content_metadata.schema]
        comparators.dispatch("schema", autogen_context.dialect.name)(
            autogen_context, upgrade_ops, schemas
        )
        return upgrade_ops

    def get_migration_code(self):
        ops = self.upgrade_steps
        mcode = render_python_code(ops)
        code = ""
        for l in mcode.split("\n"):
            if not l.strip().startswith("#"):
                code += l + "\n"
        code = "def migrate(op):\n{}".format(code)

        return code

    def update(self):
        code = self.migration_code
        migrate = _get_migrate_function(code)
        schema_name = self.context.content_metadata().schema

        with self.engine.connect() as conn:
            migration_context = MigrationContext.configure(
                conn, opts={"include_schemas": False}
            )
            op = Operations(migration_context)
            if not self.engine.dialect.has_schema(self.engine, schema_name):
                conn.execute(CreateSchema(schema_name))
            migrate(op)

    def list_update_actions(self) -> typing.List[dict]:
        return self.upgrade_steps.as_diffs()

    def close(self):
        migration_context = MigrationContext.configure(
            conn, opts={"include_schemas": False}
        )
        self.conn.close()
