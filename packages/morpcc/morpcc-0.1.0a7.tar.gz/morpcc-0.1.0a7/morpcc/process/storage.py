import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ProcessModel


class Process(morpfw.sql.Base):

    __tablename__ = "morpcc_process"

    signal = sa.Column(sa.String(length=256), index=True)
    task_id = sa.Column(morpfw.sql.GUID(), index=True)
    start = sa.Column(sa.DateTime(timezone=True), index=True)
    end = sa.Column(sa.DateTime(timezone=True), index=True)
    params = sa.Column(sajson.JSONField())
    traceback = sa.Column(sa.Text())


class ProcessStorage(morpfw.SQLStorage):
    model = ProcessModel
    orm_model = Process
