from peewee import AutoField, ForeignKeyField, CharField

from ecommquery.db.db import BaseModel
from ecommquery.db.map.definitions.Space import SpcDef


class PropDef(BaseModel):
    id = AutoField()

    spc = ForeignKeyField(
        SpcDef,
        column_name="spc_id",
        null=True,
        backref="properties",
        on_delete="SET NULL"
    )

    ref_name = CharField(max_length=255, null=True)
    type = CharField(max_length=1, null=True)
    validator_fun = CharField(max_length=255, null=True)
    flags = CharField(max_length=1, null=True)

    class Meta:
        table_name = "prop_def"
