from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_jwt.decorators import protected
from policies.models import Policy, UserAgentRule, GeographicRule, IPRangeRule, ASNRule
from redirectors.models import Path
from tortoise.exceptions import IntegrityError
import ipaddress


async def policy_edit(request, policy_id=None):
    action = False
    try:
        if request.json['name'] == '':
            response = {'error': 'Policy name cannot be blank', action: False}
            return json(response)

        # Check if we are adding a new payload or editing an existing one
        if policy_id is None:
            action = 'created'
            policy = Policy()
        else:
            action = 'modified'
            policy = await Policy.filter(pk=policy_id).first()

        policy.name = request.json['name']
        policy.notes = request.json['notes']
        await policy.save()

        # Clear out any existing rules
        await GeographicRule.filter(policy=policy).delete()
        await ASNRule.filter(policy=policy).delete()
        await IPRangeRule.filter(policy=policy).delete()
        await UserAgentRule.filter(policy=policy).delete()

        if request.json['geographic_blocklist']:
            for country_code in request.json['geographic_blocklist'].split('\n'):
                country_code = country_code.strip().upper()
                if len(country_code) == 2:
                    rule = GeographicRule()
                    rule.policy = policy
                    rule.allowlist = False
                    rule.country_code = country_code
                    await rule.save()
        if request.json['geographic_allowlist']:
            for country_code in request.json['geographic_allowlist'].split('\n'):
                country_code = country_code.strip().upper()
                if len(country_code) == 2:
                    rule = GeographicRule()
                    rule.policy = policy
                    rule.allowlist = True
                    rule.country_code = country_code
                    await rule.save()
        if request.json['ip_range_blocklist']:
            for ip_range in request.json['ip_range_blocklist'].split('\n'):
                ip_range = ip_range.strip()
                if len(ip_range) > 0:
                    try:
                        rule = IPRangeRule()
                        rule.policy = policy
                        rule.allowlist = False
                        rule.ip_range = str(ipaddress.ip_network(ip_range))
                        await rule.save()
                    except ValueError:
                        # Invalid IP range provided
                        rule = None
        if request.json['ip_range_allowlist']:
            for ip_range in request.json['ip_range_allowlist'].split('\n'):
                ip_range = ip_range.strip()
                if len(ip_range) > 0:
                    try:
                        rule = IPRangeRule()
                        rule.policy = policy
                        rule.allowlist = True
                        rule.ip_range = str(ipaddress.ip_network(ip_range))
                        await rule.save()
                    except ValueError:
                        # Invalid IP range provided
                        rule = None
        if request.json['user_agent_blocklist']:
            for user_agent in request.json['user_agent_blocklist'].split('\n'):
                user_agent = user_agent.strip()
                if len(user_agent) > 0:
                    rule = UserAgentRule()
                    rule.policy = policy
                    rule.allowlist = False
                    rule.user_agent = user_agent
                    await rule.save()
        if request.json['user_agent_allowlist']:
            for user_agent in request.json['user_agent_allowlist'].split('\n'):
                user_agent = user_agent.strip()
                if len(user_agent) > 0:
                    rule = UserAgentRule()
                    rule.policy = policy
                    rule.allowlist = True
                    rule.user_agent = user_agent
                    await rule.save()
        if request.json['asn_blocklist']:
            for asn in request.json['asn_blocklist'].split('\n'):
                asn = asn.strip()
                if len(asn) > 0:
                    rule = ASNRule()
                    rule.policy = policy
                    rule.allowlist = False
                    rule.asn_org_name = asn
                    await rule.save()
        if request.json['asn_allowlist']:
            for asn in request.json['asn_allowlist'].split('\n'):
                asn = asn.strip()
                if len(asn) > 0:
                    rule = ASNRule()
                    rule.policy = policy
                    rule.allowlist = True
                    rule.asn_org_name = asn
                    await rule.save()


        response = {'id': policy.pk, 'error': '', action: True}
        return json(response)
    except IntegrityError:
        error_message = 'Policy name {name} already exists'.format(name=request.json['name'])
        response = {'error': error_message, action: False}
        return json(response)
    except Exception:
        response = {'error': 'Unknown error occurred while adding policy', action: False}
        return json(response)


class PoliciesView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        if request.args.get('list'):
            all_policies = await Policy.all().values('name', 'id')
        else:
            all_policies = await Policy.all().values()
            for policy in all_policies:
                policy['geographic_blocklist'] = await GeographicRule.filter(policy_id=policy['id'], allowlist=False)\
                    .all().values()
                policy['geographic_allowlist'] = await GeographicRule.filter(policy_id=policy['id'], allowlist=True)\
                    .all().values()
                policy['ip_range_blocklist'] = await IPRangeRule.filter(policy_id=policy['id'], allowlist=False)\
                    .all().values()
                policy['ip_range_allowlist'] = await IPRangeRule.filter(policy_id=policy['id'], allowlist=True)\
                    .all().values()
                policy['user_agent_blocklist'] = await UserAgentRule.filter(policy_id=policy['id'], allowlist=False)\
                    .all().values()
                policy['user_agent_allowlist'] = await UserAgentRule.filter(policy_id=policy['id'], allowlist=True)\
                    .all().values()
                policy['asn_blocklist'] = await ASNRule.filter(policy_id=policy['id'], allowlist=False)\
                    .all().values()
                policy['asn_allowlist'] = await ASNRule.filter(policy_id=policy['id'], allowlist=True)\
                    .all().values()

        return json(all_policies)

    async def post(self, request):
        return await policy_edit(request)


class PolicyView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, policy_id):
        policy = await Policy.filter(pk=policy_id).first().values()

        if policy:
            policy['geographic_blocklist'] = ""
            policy['geographic_allowlist'] = ""
            policy['ip_range_blocklist'] = ""
            policy['ip_range_allowlist'] = ""
            policy['user_agent_blocklist'] = ""
            policy['user_agent_allowlist'] = ""
            policy['asn_blocklist'] = ""
            policy['asn_allowlist'] = ""

            geographic_block_rules = await GeographicRule.filter(policy_id=policy['id'], allowlist=False).all().values()
            for rule in geographic_block_rules:
                policy['geographic_blocklist'] += rule['country_code'] + "\n"
            geographic_allow_rules = await GeographicRule.filter(policy_id=policy['id'], allowlist=True).all().values()
            for rule in geographic_allow_rules:
                policy['geographic_allowlist'] += rule['country_code'] + "\n"

            ip_range_block_rules = await IPRangeRule.filter(policy_id=policy['id'], allowlist=False).all().values()
            for rule in ip_range_block_rules:
                policy['ip_range_blocklist'] += rule['ip_range'] + "\n"
            ip_range_allow_rules = await IPRangeRule.filter(policy_id=policy['id'], allowlist=True).all().values()
            for rule in ip_range_allow_rules:
                policy['ip_range_allowlist'] += rule['ip_range'] + "\n"

            user_agent_block_rules = await UserAgentRule.filter(policy_id=policy['id'], allowlist=False).all().values()
            for rule in user_agent_block_rules:
                policy['user_agent_blocklist'] += rule['user_agent'] + "\n"
            user_agent_allow_rules = await UserAgentRule.filter(policy_id=policy['id'], allowlist=True).all().values()
            for rule in user_agent_allow_rules:
                policy['user_agent_allowlist'] += rule['user_agent'] + "\n"

            asn_block_rules = await ASNRule.filter(policy_id=policy['id'], allowlist=False).all().values()
            for rule in asn_block_rules:
                policy['asn_blocklist'] += rule['asn_org_name'] + "\n"
            asn_allow_rules = await ASNRule.filter(policy_id=policy['id'], allowlist=True).all().values()
            for rule in asn_allow_rules:
                policy['asn_allowlist'] += rule['asn_org_name'] + "\n"

            return json(policy)
        else:
            response = {'error': 'Policy not found'}
            return json(response)

    async def put(self, request, policy_id):
        return await policy_edit(request, policy_id)

    async def delete(self, request, policy_id):
        policy = await Policy.filter(pk=policy_id).first()
        if policy:
            # Reset any paths to no policy that had this policy assigned
            paths = await Path.filter(policy_id=policy_id)
            for path in paths:
                path.policy_id = None
                await path.save()
            paths = await Path.filter(policy_id=policy_id)
            for path in paths:
                path.policy_id = None
                await path.save()

            await policy.delete()
            response = {'id': policy.pk, 'deleted': True}
            return json(response)
        else:
            response = {'error': 'Policy not found', 'deleted': False}
            return json(response)
