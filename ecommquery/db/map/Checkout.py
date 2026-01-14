from peewee import IntegerField, DateTimeField, AutoField, ForeignKeyField, CompositeKey, SQL

from ecommquery.db.db import BaseModel
from ecommquery.db.map.Object import Obj
from ecommquery.db.map.definitions.Sources import CheckoutSourceDef


class ObjCheckout(BaseModel):
    id = AutoField()
    # obj = ForeignKeyField(
    #     Obj,
    #     column_name="obj_id",
    #     null=False,
    #     backref="objs"
    # )

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
