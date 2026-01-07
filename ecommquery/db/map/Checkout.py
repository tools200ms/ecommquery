from peewee import IntegerField, DateTimeField, AutoField, ForeignKeyField, CompositeKey, SQL

from ecommquery.db.db import BaseModel
from ecommquery.db.map.definitions.Sources import CheckoutSourceDef


class ObjCheckout(BaseModel):
    id = AutoField()
    #obj_id = IntegerField()

    timestamp = DateTimeField(
        constraints=[SQL("DEFAULT (datetime('now', 'localtime'))")]
    )

    src = ForeignKeyField(
        CheckoutSourceDef,
        column_name="src_id",
        null=True,
        backref="checkouts",
        on_delete="SET NULL"
    )

    class Meta:
        table_name = "obj_checkout"
