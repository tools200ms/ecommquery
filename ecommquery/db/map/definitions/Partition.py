from peewee import SmallIntegerField, ForeignKeyField, CharField, AutoField

from ecommquery.db.db import BaseModel
from ecommquery.db.map.definitions.Space import SpcDef


class PartDef(BaseModel):
    id = AutoField()

    spc = ForeignKeyField(
        SpcDef,
        backref="parts",
        column_name="spc_id",
        on_delete="RESTRICT"
    )

    name = CharField(max_length=64, null=True)

    class Meta:
        table_name = "part_def"
        indexes = (
            (("id", "spc", "name"), True),  # UNIQUE (id, spc_id, name)
        )