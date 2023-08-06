import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import SettingModel


class Setting(morpfw.sql.Base):

    __tablename__ = "morpcc_setting"

    key = sa.Column(sa.String(length=256), index=True)
    data = sa.Column(sajson.JSONField())


class SettingStorage(morpfw.SQLStorage):
    model = SettingModel
    orm_model = Setting
