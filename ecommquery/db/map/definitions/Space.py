from peewee import SmallIntegerField, CharField, AutoField

from ecommquery.db.db import BaseModel


class SpcDef(BaseModel):
    id = AutoField()
    name = CharField(max_length=16, null=True)

    class Meta:
        table_name = "spc_def"
        indexes = (
            (("id", "name"), True),  # UNIQUE (id, name)
        )
