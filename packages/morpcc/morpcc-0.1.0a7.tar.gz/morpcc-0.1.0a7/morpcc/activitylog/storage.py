import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ActivityLogModel


class ActivityLog(morpfw.sql.Base):

    __tablename__ = "morpcc_activitylog"

    userid = sa.Column(morpfw.sql.GUID())
    resource_uuid = sa.Column(morpfw.sql.GUID())
    resource_type = sa.Column(sa.String(length=256))
    view_name = sa.Column(sa.String(length=128))
    source_ip = sa.Column(sa.String(length=64))
    activity = sa.Column(sa.Text())


class ActivityLogStorage(morpfw.SQLStorage):
    model = ActivityLogModel
    orm_model = ActivityLog
