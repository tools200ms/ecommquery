from peewee import *

from ecommquery.db.db import BaseModel
from ecommquery.db.map.definitions.Partition import PartDef


class CheckoutSourceDef(BaseModel):
    id = AutoField()

    name = CharField(max_length=256, null=True)

    part = ForeignKeyField(
        PartDef,
        column_name="part_id",
        backref="checkout_sources",
        on_delete="RESTRICT"
    )

    function = CharField(null=True)

    triggered_by = SmallIntegerField(null=True)

    class Meta:
        table_name = "checkout_sources_def"
