from peewee import ForeignKeyField, CharField, IntegerField

from ecommquery.db.db import BaseModel
from ecommquery.db.map.Checkout import ObjCheckout
from ecommquery.db.map.definitions.Property import PropDef


class ObjPropNoChange(BaseModel):
    prop = ForeignKeyField(
        PropDef,
        column_name="prop_id",
        backref="nochange_props",
        on_delete="CASCADE"
    )

    checkout = ForeignKeyField(
        ObjCheckout,
        column_name="checkout_id",
        backref="nochange_props",
        on_delete="CASCADE"
    )

    class Meta:
        table_name = "obj_prop_nochange"
        primary_key = False
        indexes = (
            (("prop", "checkout"), True),  # UNIQUE (prop_id, checkout_id)
        )

class ObjPropText(BaseModel):
    prop = ForeignKeyField(
        PropDef,
        column_name="prop_id",
        backref="text_props",
        on_delete="CASCADE"
    )

    checkout = ForeignKeyField(
        ObjCheckout,
        column_name="checkout_id",
        backref="text_props",
        on_delete="CASCADE"
    )

    value = CharField(max_length=32, null=True)

    class Meta:
        table_name = "obj_prop_text"
        primary_key = False
        indexes = (
            (("prop", "checkout"), True),  # UNIQUE (prop_id, checkout_id)
        )

class ObjPropInt(BaseModel):
    prop = ForeignKeyField(
        PropDef,
        column_name="prop_id",
        backref="int_props",
        on_delete="CASCADE"
    )

    checkout = ForeignKeyField(
        ObjCheckout,
        column_name="checkout_id",
        backref="int_props",
        on_delete="CASCADE"
    )

    value = IntegerField(null=True)

    class Meta:
        table_name = "obj_prop_int"
        primary_key = False
        indexes = (
            (("prop", "checkout"), True),  # UNIQUE (prop_id, checkout_id)
        )

