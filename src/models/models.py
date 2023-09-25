from tortoise.models import Model
from tortoise import fields


class Url(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=128)
    short_url = fields.CharField(max_length=64)
    click = fields.IntField()
    create_date = fields.DatetimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return "(url='%s'); (short_url=%s)" % (self.url, self.short_url)