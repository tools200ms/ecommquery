from peewee import CharField, DateTimeField, SQL

from ecommquery.db.db import BaseModel


class Comment(BaseModel):
    msg = CharField(max_length=4096)

    msg_date = DateTimeField(
        constraints=[SQL("DEFAULT (datetime('now', 'localtime'))")]
    )

    class Meta:
        table_name = "comments"
        primary_key = False

