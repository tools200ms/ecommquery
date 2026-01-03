
class SpcDef(BaseModel):
    id = SmallIntegerField(primary_key=True)
    name = CharField(max_length=16, null=True)

    class Meta:
        table_name = "spc_def"
        indexes = (
            (("id", "name"), True),  # UNIQUE (id, name)
        )
