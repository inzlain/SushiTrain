from tortoise import fields, timezone, Model


class RequestLog(Model):
    allowed = fields.BooleanField(default=False)
    action = fields.CharField(max_length=20, null=False, blank=False, default='404')
    datetime = fields.DatetimeField(default=timezone.now, blank=False, null=False)

    redirector = fields.ForeignKeyField('models.Redirector', related_name='request_log', on_delete=fields.SET_NULL, null=True, blank=True)
    path = fields.ForeignKeyField('models.Path', related_name='request_log', on_delete=fields.SET_NULL, null=True, blank=True)
    redirector_hostname = fields.CharField(max_length=255, default='')
    redirector_path = fields.CharField(max_length=2048, default='')

    request_method = fields.TextField(default='')
    request_headers = fields.TextField(default='')
    request_body = fields.BinaryField(blank=True, null=True)
    request_country_code = fields.CharField(max_length=10, default='')
    request_user_agent = fields.TextField(default='')
    request_hostname = fields.CharField(max_length=255, default='')
    request_ip = fields.CharField(max_length=50, default='')
    request_asn_org_name = fields.TextField(default='')

    response_status = fields.SmallIntField(default=0)
    response_headers = fields.TextField(default='')
    response_body = fields.BinaryField(blank=True, null=True)

    payload = fields.ForeignKeyField('models.Payload', related_name='request_log', on_delete=fields.SET_NULL, null=True, blank=True)
    file = fields.ForeignKeyField('models.File', related_name='request_log', on_delete=fields.SET_NULL, null=True, blank=True)

    async def add_message(self, message):
        request_log_message = RequestLogMessage()
        request_log_message.request_log = self
        request_log_message.message = message
        await request_log_message.save()


class RequestLogMessage(Model):
    request_log = fields.ForeignKeyField('models.RequestLog', related_name='request_log', on_delete=fields.CASCADE)
    datetime = fields.DatetimeField(default=timezone.now, blank=False, null=False)
    message = fields.TextField()
