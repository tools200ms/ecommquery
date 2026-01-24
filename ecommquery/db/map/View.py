from peewee import ForeignKeyField, CharField, IntegerField

from ecommquery.db.db import BaseModel
from ecommquery.db.map.Checkout import ObjCheckout
from ecommquery.db.map.Object import Obj
from ecommquery.db.map.definitions.Property import PropDef
from ecommquery.db.map.definitions.Sources import CheckoutSourceDef


class ObjIntLatestView(BaseModel):
    obj = ForeignKeyField(
        Obj,
        column_name="obj_id",
        backref="nochange_props")

    prop = ForeignKeyField(
        PropDef,
        column_name="prop_id",
        backref="nochange_props"
    )

    checkout = ForeignKeyField(
        ObjCheckout,
        column_name="checkout_id",
        backref="int_props"
    )

    value = IntegerField(null=True)

    class Meta:
        table_name = "obj_int_latest"
        primary_key = False  # views typically have no PK

class ObjTextLatestView(BaseModel):
    obj = ForeignKeyField(
        Obj,
        column_name="obj_id",
        backref="nochange_props")

    prop = ForeignKeyField(
        PropDef,
        column_name="prop_id",
        backref="nochange_props"
    )

    checkout = ForeignKeyField(
        ObjCheckout,
        column_name="checkout_id",
        backref="int_props"
    )

    value = CharField(null=True)

    class Meta:
        table_name = "obj_text_latest"
        primary_key = False  # views typically have no PK


class ObjCombLatestView(BaseModel):
    obj = ForeignKeyField(
        Obj,
        column_name="obj_id",
        backref="nochange_props")

    prop = ForeignKeyField(
        PropDef,
        column_name="prop_id",
        backref="nochange_props"
    )

    checkout = ForeignKeyField(
        ObjCheckout,
        column_name="checkout_id",
        backref="int_props"
    )

    valuet = CharField(null=True)
    valuei = IntegerField(null=True)

    class Meta:
        table_name = "_obj_comb_latest"
        primary_key = False  # views typically have no PK


class ChkPropAllView(BaseModel):
    obj = ForeignKeyField(
        Obj,
        column_name="obj_id",
        backref="nochange_props")

    prop = ForeignKeyField(
        PropDef,
        column_name="prop_id",
        backref="nochange_props"
    )

    checkout = ForeignKeyField(
        ObjCheckout,
        column_name="checkout_id",
        backref="int_props"
    )

    src = ForeignKeyField(
        CheckoutSourceDef,
        column_name="src_id"
    )

    valuet = CharField(null=True)
    valuei = IntegerField(null=True)

    class Meta:
        table_name = "checkout_prop_all"
        primary_key = False  # views typically have no PK

