import sanic_jwt.decorators
from sanic import Sanic
from sanic.response import json, text
from sanic.views import HTTPMethodView
from sanic_jwt.decorators import protected
from redirectors.models import Redirector, Path, RedirectorHeader, PathAllowHeader, PathDenyHeader
from payloads.models import Payload
from policies.models import Policy
from files.models import File
from tortoise.exceptions import IntegrityError


async def redirector_edit(request, redirector_id=None):
    try:
        action = 'validated'

        if request.json['hostname'] == '':
            response = {'error': 'Redirector hostname cannot be blank', action: False}
            return json(response)

        if redirector_id is None:
            action = 'created'
            redirector = Redirector()
        else:
            action = 'modified'
            redirector = await Redirector.filter(pk=redirector_id).first()

        redirector.hostname = request.json['hostname']
        redirector.host_header = request.json['host_header']
        redirector.notes = request.json['notes']

        try:
            port = int(request.json['port'])
            redirector.port = port
        except ValueError:
            response = {'error': 'Redirector port must be a number', action: False}
            return json(response)

        if request.json['https'] == 'yes':
            redirector.https = True
        else:
            redirector.https = False

        if 'default_policy_id' in request.json and request.json['default_policy_id'] and request.json['default_policy_id'] != 'null':
            redirector.default_policy_id = request.json['default_policy_id']
        else:
            redirector.default_policy_id = None

        redirector.default_logging = request.json['default_logging']
        redirector.default_logging_request_body = request.json['default_logging_request_body']
        redirector.default_logging_response_body = request.json['default_logging_response_body']

        await redirector.save()

        # Clear out any existing headers
        await RedirectorHeader.filter(redirector=redirector).all().delete()

        # Process the headers
        if request.json['headers'] != '':
            for line in request.json['headers'].splitlines():
                header = line.split(':', 1)

                if len(header) == 2 and header[0] != '':
                    redirector_header = RedirectorHeader()
                    redirector_header.redirector = redirector
                    redirector_header.header = header[0].strip()
                    redirector_header.value = header[1].strip()
                    await redirector_header.save()

        response = {'id': redirector.pk, 'error': '', action: True}
        return json(response)

    except IntegrityError:
        response = {'error': 'Redirector hostname already exists', action: False}
        return json(response)
    except Exception:
        response = {'error': 'Unknown error occurred while adding redirector', action: False}
        return json(response)


async def path_edit(request, path_id=None):
    try:
        action = 'validated'

        if request.json['path'] == '':
            response = {'error': 'Path cannot be blank', action: False}
            return json(response)
        if request.json['path'][0] != '/':
            response = {'error': 'Path must start with leading /', action: False}
            return json(response)
        if request.json['redirector_id'] == '':
            response = {'error': 'Redirector must be specified', action: False}
            return json(response)
        if not await Redirector.exists(pk=request.json['redirector_id']):
            response = {'error': 'Redirector doesn\'t exist', action: False}
            return json(response)

        if path_id is None:
            action = 'created'
            path = Path()
        else:
            action = 'modified'
            path = await Path.filter(pk=path_id).first()

        path.path = request.json['path']
        path.redirector_id = request.json['redirector_id']
        path.notes = request.json['notes']
        path.enabled = request.json['enabled']

        path.logging = request.json['logging']
        path.logging_request_body = request.json['logging_request_body']
        path.logging_response_body = request.json['logging_response_body']

        path.slack_notifications = request.json['slack_notifications']
        path.slack_template = request.json['slack_template']

        if 'policy_id' in request.json and request.json['policy_id'] and request.json['policy_id'] != 'null':
            path.policy_id = request.json['policy_id']
        else:
            path.policy_id = None

        path.allow_template = request.json['allow_template']
        path.deny_template = request.json['deny_template']

        path.allow_action = request.json['allow_action']
        path.deny_action = request.json['deny_action']

        if path.allow_action == 'payload':
            if 'payload' in request.json and request.json['payload'] and request.json['payload'] != 'null':
                path.payload_id = int(request.json['payload'])
            else:
                path.payload_id = None
                path.allow_action = '404'

        if path.deny_action == 'payload':
            if 'deny_payload' in request.json and request.json['deny_payload']and request.json['deny_payload'] != 'null':
                path.deny_payload_id = int(request.json['deny_payload'])
            else:
                path.deny_payload_id = None
                path.deny_action = '404'

        if path.allow_action == 'file':
            if 'file' in request.json and request.json['file'] and request.json['file'] != 'null':
                path.file_id = int(request.json['file'])
            else:
                path.file_id = None
                path.allow_action = '404'

        if path.deny_action == 'file':
            if 'deny_file' in request.json and request.json['deny_file'] and request.json['deny_file'] != 'null':
                path.deny_file_id = int(request.json['deny_file'])
            else:
                path.deny_file_id = None
                path.deny_action = '404'

        if path.allow_action == 'passthrough':
            if 'passthrough_url' in request.json and request.json['passthrough_url'] and request.json['passthrough_url'] != 'null':
                path.passthrough_url = request.json['passthrough_url']
                path.passthrough_request_headers = request.json['passthrough_request_headers']
                path.passthrough_request_body = request.json['passthrough_request_body']
                path.passthrough_response_headers = request.json['passthrough_response_headers']
            else:
                path.passthrough_url = ''
                path.allow_action = '404'

        if path.deny_action == 'passthrough':
            if 'deny_passthrough_url' in request.json and request.json['deny_passthrough_url'] and request.json['deny_passthrough_url'] != 'null':
                path.deny_passthrough_url = request.json['deny_passthrough_url']
                path.deny_passthrough_request_headers = request.json['deny_passthrough_request_headers']
                path.deny_passthrough_request_body = request.json['deny_passthrough_request_body']
                path.deny_passthrough_response_headers = request.json['deny_passthrough_response_headers']
            else:
                path.deny_passthrough_url = ''
                path.deny_action = '404'

        if path.allow_action == '302':
            if 'redirect_url' in request.json and request.json['redirect_url'] and request.json[
                'redirect_url'] != 'null':
                path.redirect_url = request.json['redirect_url']
            else:
                path.redirect_url = ''
                path.allow_action = '404'

        if path.deny_action == '302':
            if 'deny_redirect_url' in request.json and request.json['deny_redirect_url'] and request.json[
                'deny_redirect_url'] != 'null':
                path.deny_redirect_url = request.json['deny_redirect_url']
            else:
                path.deny_redirect_url = ''
                path.deny_action = '404'

        await path.save()

        # Clear out any existing allow headers
        await PathAllowHeader.filter(path=path).all().delete()

        # Process the allow headers
        if request.json['allow_headers'] != '':
            for line in request.json['allow_headers'].splitlines():
                header = line.split(':', 1)

                if len(header) == 2 and header[0] != '':
                    allow_header = PathAllowHeader()
                    allow_header.path = path
                    allow_header.header = header[0].strip()
                    allow_header.value = header[1].strip()
                    await allow_header.save()

        # Clear out any existing deny headers
        await PathDenyHeader.filter(path=path).all().delete()

        # Process the deny headers
        if request.json['deny_headers'] != '':
            for line in request.json['deny_headers'].splitlines():
                header = line.split(':', 1)

                if len(header) == 2 and header[0] != '':
                    deny_header = PathDenyHeader()
                    deny_header.path = path
                    deny_header.header = header[0].strip()
                    deny_header.value = header[1].strip()
                    await deny_header.save()

        response = {'id': path.pk, 'error': '', action: True}
        return json(response)
    except IntegrityError:
        response = {'error': 'Path already exists', action: False}
        return json(response)
    except Exception:
        response = {'error': 'Unknown error occurred while adding path', action: False}
        return json(response)


class RedirectorsView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        if request.args.get('list'):
            all_redirectors = await Redirector.all().order_by('hostname').values('hostname', 'id')
            return json(all_redirectors)
        else:
            all_redirectors = await Redirector.all().order_by('hostname').values()
            for redirector in all_redirectors:
                if redirector['https']:
                    redirector['https'] = 'yes'
                else:
                    redirector['https'] = 'no'

                redirector['paths'] = await Path.filter(redirector__id=redirector['id']).all().order_by('path').values()
                for path in redirector['paths']:
                    if path['policy_id'] is not None:
                        policy = await Policy.filter(id=path['policy_id']).first()
                        path['policy_name'] = policy.name
                    if path['payload_id'] is not None:
                        payload = await Payload.filter(id=path['payload_id']).first()
                        path['payload_name'] = payload.name
                    if path['deny_payload_id'] is not None:
                        payload = await Payload.filter(id=path['deny_payload_id']).first()
                        path['deny_payload_name'] = payload.name
                    if path['file_id'] is not None:
                        file = await File.filter(id=path['file_id']).first()
                        path['file_name'] = file.name
                    if path['deny_file_id'] is not None:
                        file = await File.filter(id=path['deny_file_id']).first()
                        path['deny_file_name'] = file.name

                    if redirector['https']:
                        url = 'https://' + redirector['hostname']
                        if redirector['port'] == 443:
                            url = url + path['path']
                        else:
                            url = url + ':' + str(redirector['port']) + path['path']
                    else:
                        url = 'https://' + path['redirector__hostname']
                        if redirector['port'] == 80:
                            url = url + path['path']
                        else:
                            url = url + ':' + str(redirector['port']) + path['path']
                    path['url'] = url

            return json(all_redirectors)

    async def post(self, request):
        return await redirector_edit(request)


class RedirectorView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, redirector_id):
        redirector = await Redirector.filter(pk=redirector_id).first().values()

        if redirector:
            if redirector['https']:
                redirector['https'] = 'yes'
            else:
                redirector['https'] = 'no'

            redirector['paths'] = await Path.filter(redirector__id=redirector_id).all().order_by('path').values()

            headers = await RedirectorHeader.filter(redirector__id=redirector_id).all()
            redirector['headers'] = ''
            for header in headers:
                redirector['headers'] += header.header + ': ' + header.value + '\n'
            return json(redirector)
        else:
            response = {'error': 'Redirector not found'}
            return json(response)

    async def put(self, request, redirector_id):
        return await redirector_edit(request, redirector_id)

    async def delete(self, request, redirector_id):
        redirector = await Redirector.filter(pk=redirector_id).first()
        if redirector:
            await redirector.delete()
            response = {'id': redirector.pk, 'deleted': True}
            return json(response)
        else:
            response = {'error': 'Redirector not found', 'deleted': False}
            return json(response)


class RedirectorPathsView(HTTPMethodView):
    decorators = [protected()]


    async def get(self, request, redirector_id):
        all_paths = await Path.filter(redirector_id=redirector_id).all().values()
        return json(all_paths)


class RedirectorDeployView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, redirector_id, redirector_type):
        from jinja2 import Environment, FileSystemLoader
        management = Sanic.get_app("Management")

        try:
            environment = Environment(loader=FileSystemLoader("redirectors/templates/"))

            redirector = await Redirector.filter(pk=redirector_id).first()
            redirector_paths = await Path.filter(redirector_id=redirector_id).all().values('path')
            redirector_paths_list = []
            for redirector_path in redirector_paths:
                redirector_paths_list.append(redirector_path['path'])

            if redirector_type == "nginx":
                template = environment.get_template("nginx.jinja")
            elif redirector_type == "apache":
                template = environment.get_template("apache.jinja")
            elif redirector_type == "cloudfront_lambda":
                template = environment.get_template("cloudfront_lambda.jinja")
            elif redirector_type == "cloudfront_function":
                template = environment.get_template("cloudfront_function.jinja")
            else:
                return text("Invalid redirector type provided")

            return text(template.render(delivery_hostname=management.config['DELIVERY_HOSTNAME'],
                                        delivery_port=str(management.config['DELIVERY_PORT']),
                                        delivery_path=management.config['DELIVERY_PATH'],
                                        redirector_hostname=redirector.hostname,
                                        redirector_paths=redirector_paths_list))
        except Exception:
            return text("Error generating redirector configuration")


class PathsView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        all_paths = await Path.all().values()
        return json(all_paths)

    async def post(self, request):
        return await path_edit(request)


class PathsDisableAll(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        paths = await Path.all()
        for path in paths:
            path.enabled = False
            await path.save()
        response = {'enabled': False}
        return json(response)


class PathsEnableAllView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        paths = await Path.all()
        for path in paths:
            path.enabled = True
            await path.save()
        response = {'enabled': True}
        return json(response)


class URLsView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        all_paths = await Path.all().order_by('redirector__hostname').order_by('path') \
            .values('redirector__hostname', 'redirector__port', 'redirector__https', 'path', 'id')
        all_urls = []
        for path in all_paths:
            if path['redirector__https']:
                url = 'https://' + path['redirector__hostname']
                if path['redirector__port'] == 443:
                    url = url + path['path']
                else:
                    url = url + ':' + str(path['redirector__port']) + path['path']
            else:
                url = 'https://' + path['redirector__hostname']
                if path['redirector__port'] == 80:
                    url = url + path['path']
                else:
                    url = url + ':' + str(path['redirector__port']) + path['path']
            all_urls.append(url)
        return json(all_urls)


class PathView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, path_id):
        path = await Path.filter(pk=path_id).first().values()
        if path:
            redirector_headers = await RedirectorHeader.filter(redirector_id=path['redirector_id']).all()
            path['redirector_headers'] = ''
            for header in redirector_headers:
                path['redirector_headers'] += header.header + ': ' + header.value + '\n'

            allow_headers = await PathAllowHeader.filter(path_id=path_id).all()
            path['allow_headers'] = ''
            for header in allow_headers:
                path['allow_headers'] += header.header + ': ' + header.value + '\n'

            deny_headers = await PathDenyHeader.filter(path_id=path_id).all()
            path['deny_headers'] = ''
            for header in deny_headers:
                path['deny_headers'] += header.header + ': ' + header.value + '\n'

            return json(path)
        else:
            response = {'error': 'Path ID not found'}
            return json(response)

    async def put(self, request, path_id):
        return await path_edit(request, path_id)

    async def delete(self, request, path_id):
        path = await Path.filter(pk=path_id).first()
        if path:
            await path.delete()
            response = {'id': path.pk, 'deleted': True}
            return json(response)
        else:
            response = {'error': 'Path ID not found', 'deleted': False}
            return json(response)
