from peewee import AutoField

from ecommquery.db.db import BaseModel


class Obj(BaseModel):
    id = AutoField()

    class Meta:
        table_name = "obj"
