from tortoise.models import Model
from tortoise import fields


class Policy(Model):
    name = fields.CharField(max_length=255, unique=True, blank=False)
    notes = fields.TextField(default='', blank=True)

    user_agent_rules: fields.ReverseRelation["UserAgentRule"]
    geographic_rules: fields.ReverseRelation["GeographicRule"]
    asn_rules: fields.ReverseRelation["ASNRule"]
    ip_range_rules: fields.ReverseRelation["IPRangeRule"]

    def __str__(self):
        return self.name


class UserAgentRule(Model):
    policy = fields.ForeignKeyField('models.Policy', related_name='user_agent_rules', on_delete=fields.CASCADE)
    allowlist = fields.BooleanField(default=True)
    user_agent = fields.TextField(blank=False, null=False)


class GeographicRule(Model):
    policy = fields.ForeignKeyField('models.Policy', related_name='geographic_rules', on_delete=fields.CASCADE)
    allowlist = fields.BooleanField(default=True)
    country_code = fields.CharField(max_length=2, blank=False, null=False)


class ASNRule(Model):
    policy = fields.ForeignKeyField('models.Policy', related_name='asn_rules', on_delete=fields.CASCADE)
    allowlist = fields.BooleanField(default=True)
    asn_org_name = fields.TextField(blank=False, null=False)


class IPRangeRule(Model):
    policy = fields.ForeignKeyField('models.Policy', related_name='ip_range_rules', on_delete=fields.CASCADE)
    allowlist = fields.BooleanField(default=True)
    ip_range = fields.TextField(blank=False, null=False)
