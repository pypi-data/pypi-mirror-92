import morpfw
import morpfw.sql
import sqlalchemy as sa
import sqlalchemy_jsonfield as sajson

from .model import IndexModel


class Index(morpfw.sql.Base):

    __tablename__ = "morpcc_index"

    name = sa.Column(sa.String(256), index=True)
    title = sa.Column(sa.String(length=256))
    type = sa.Column(sa.String(256))
    description = sa.Column(sa.Text())


class IndexStorage(morpfw.SQLStorage):
    model = IndexModel
    orm_model = Index
