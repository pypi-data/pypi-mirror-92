import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import ObjectPermissionAssignmentModel


class ObjectPermissionAssignment(morpfw.sql.Base):

    __tablename__ = "morpcc_objectpermissionassignment"

    object_uuid = sa.Column(morpfw.sql.GUID())
    permission = sa.Column(sa.String(length=256))
    roles = sa.Column(sajson.JSONField())
    rule = sa.Column(sa.String(length=24))
    enabled = sa.Column(sa.Boolean())


class ObjectPermissionAssignmentStorage(morpfw.SQLStorage):
    model = ObjectPermissionAssignmentModel
    orm_model = ObjectPermissionAssignment
