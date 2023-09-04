from tortoise.models import Model
from tortoise import fields, timezone


class Payload(Model):
    name = fields.CharField(max_length=255, unique=True, blank=False)
    notes = fields.TextField(default='', blank=True)

    modules: fields.ReverseRelation["Module"]
    log: fields.ReverseRelation["Log"]

    def __str__(self):
        return self.name


class PayloadLog(Model):
    payload = fields.ForeignKeyField('models.Payload', related_name='log', on_delete=fields.CASCADE)
    manual = fields.BooleanField(default=False, null=False)
    output = fields.BinaryField(null=False, blank=True)
    size = fields.BigIntField(null=False, blank=False, default=0)
    hash = fields.CharField(max_length=64, blank=False, null=False)
    log = fields.TextField(default='', blank=True, null=False)
    datetime = fields.DatetimeField(default=timezone.now, blank=False, null=False)

    def __str__(self):
        return self.name


class Module(Model):
    payload = fields.ForeignKeyField('models.Payload', related_name='modules', on_delete=fields.CASCADE)
    name = fields.TextField(default='')  # We keep this as a loose relationship by name rather than a foreign key to allow recovery from module loading failures
    order = fields.IntField(blank=False, default=100000)

    options: fields.ReverseRelation["ModuleOption"]
    ordering = ["order", "id"]

    def __str__(self):
        return self.payload.name + " - " + self.name


class ModuleOption(Model):
    module = fields.ForeignKeyField('models.Module', related_name='options', on_delete=fields.CASCADE)
    name = fields.TextField(blank=False, null=False)
    value = fields.TextField(default='', blank=True, null=False)
    is_file = fields.BooleanField(default=False)

    def __str__(self):
        return self.name + " - " + self.value


class ModuleLibrary(Model):
    name = fields.CharField(max_length=255, unique=True, blank=False)
    description = fields.TextField()
    author = fields.TextField()
    supports_input = fields.BooleanField(default=False)

    options: fields.ReverseRelation["ModuleOptionLibrary"]

    def __str__(self):
        return self.name


class ModuleOptionLibrary(Model):
    module = fields.ForeignKeyField('models.ModuleLibrary', related_name='options', on_delete=fields.CASCADE)
    name = fields.TextField(blank=False, null=False)
    description = fields.TextField(default='', blank=False, null=False)
    type = fields.TextField(default='text', blank=True, null=False)
    required = fields.BooleanField(default=True)
    default_value = fields.TextField(default='', blank=True, null=False)

    def __str__(self):
        return self.name
