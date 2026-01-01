from peewee import CharField, DateTimeField, SQL


def Comment(DB):
    msg = CharField(max_length=4096)

    msg_date = DateTimeField(
        constraints=[SQL("DEFAULT (datetime('now', 'localtime'))")]
    )

    class Meta:
        db_table = "comment"