from tortoise.models import Model
from tortoise import fields


class Redirector(Model):
    hostname = fields.CharField(max_length=255, unique=True, blank=False)
    host_header = fields.CharField(max_length=255, default='', blank=True)
    https = fields.BooleanField(default=True, null=False, blank=False)
    port = fields.SmallIntField(default=443, null=False, blank=False)
    default_policy = fields.ForeignKeyField('models.Policy', related_name='default_policy', null=True, on_delete=fields.SET_NULL)
    default_logging = fields.BooleanField(default=True, blank=False)
    default_logging_request_body = fields.BooleanField(default=True, blank=False)
    default_logging_response_body = fields.BooleanField(default=True, blank=False)

    notes = fields.TextField(default='', blank=True)
    # Add Owner/Operator field and link to users model?

    paths: fields.ReverseRelation["Path"]
    headers: fields.ReverseRelation["RedirectorHeader"]

    async def get_paths(self):
        return await Path.filter(redirector__id=Redirector[self.pk]).all().order_by('path').values()

    def __str__(self):
        return self.hostname


class RedirectorHeader(Model):
    redirector = fields.ForeignKeyField('models.Redirector', related_name='headers', on_delete=fields.CASCADE)
    header = fields.TextField(default='', blank=False, null=False)
    value = fields.TextField(default='', blank=True, null=False)


class Path(Model):
    path = fields.CharField(max_length=2048, blank=False, default='/')
    redirector = fields.ForeignKeyField('models.Redirector', related_name='paths', on_delete=fields.CASCADE)
    enabled = fields.BooleanField(default=True)
    notes = fields.TextField(default='', blank=True)
    policy = fields.ForeignKeyField('models.Policy', related_name='policy', null=True, on_delete=fields.SET_NULL)
    allow_action = fields.CharField(max_length=20, null=False, blank=False, default='payload')
    deny_action = fields.CharField(max_length=20, null=False, blank=False, default='404')
    payload = fields.ForeignKeyField('models.Payload', related_name='payload', null=True, on_delete=fields.SET_NULL)
    deny_payload = fields.ForeignKeyField('models.Payload', related_name='deny_payload', null=True, on_delete=fields.SET_NULL)
    file = fields.ForeignKeyField('models.File', related_name='file', null=True, on_delete=fields.SET_NULL)
    deny_file = fields.ForeignKeyField('models.File', related_name='deny_file', null=True, on_delete=fields.SET_NULL)
    passthrough_url = fields.TextField(default='', blank=True)
    passthrough_request_headers = fields.BooleanField(default=True, blank=False)
    passthrough_request_body = fields.BooleanField(default=True, blank=False)
    passthrough_response_headers = fields.BooleanField(default=True, blank=False)
    deny_passthrough_url = fields.TextField(default='', blank=True)
    deny_passthrough_request_headers = fields.BooleanField(default=True, blank=False)
    deny_passthrough_request_body = fields.BooleanField(default=True, blank=False)
    deny_passthrough_response_headers = fields.BooleanField(default=True, blank=False)
    redirect_url = fields.TextField(default='', blank=True)
    deny_redirect_url = fields.TextField(default='', blank=True)
    allow_template = fields.TextField(default='', blank=True)
    deny_template = fields.TextField(default='', blank=True)
    logging = fields.BooleanField(default=True, blank=False)
    logging_request_body = fields.BooleanField(default=True, blank=False)
    logging_response_body = fields.BooleanField(default=True, blank=False)
    slack_notifications = fields.BooleanField(default=False, blank=False)
    slack_template = fields.TextField(default='', blank=True)

    allow_headers: fields.ReverseRelation["PathAllowHeader"]
    deny_headers: fields.ReverseRelation["PathDenyHeader"]

    class Meta:
        table = "unique_redirector_path"
        unique_together = (("redirector", "path"), )

    def __str__(self):
        return self.redirector.hostname + self.path


class PathAllowHeader(Model):
    path = fields.ForeignKeyField('models.Path', related_name='allow_headers', on_delete=fields.CASCADE)
    header = fields.TextField(default='', blank=False, null=False)
    value = fields.TextField(default='', blank=True, null=False)


class PathDenyHeader(Model):
    path = fields.ForeignKeyField('models.Path', related_name='deny_headers', on_delete=fields.CASCADE)
    header = fields.TextField(default='', blank=False, null=False)
    value = fields.TextField(default='', blank=True, null=False)

