from tortoise.models import Model
from tortoise import fields


class File(Model):
    name = fields.TextField(blank=False, null=False)
    bytes = fields.BinaryField(blank=True, null=False)
    size = fields.BigIntField(null=False, blank=False, default=0)
    hash = fields.CharField(max_length=64, blank=True)
