import math
from sanic.response import json, raw
from sanic.views import HTTPMethodView
from sanic_jwt.decorators import protected
from payloads.models import Payload, PayloadLog, Module, ModuleOption, ModuleLibrary, ModuleOptionLibrary
from payloads.generator import generate_payload
from redirectors.models import Path
from tortoise.exceptions import IntegrityError


async def payload_edit(request, payload_id=None):
    action = False
    try:
        if request.json['name'] == '':
            response = {'error': 'Payload name cannot be blank', action: False}
            return json(response)

        # Check if we are adding a new payload or editing an existing one
        if payload_id is None:
            action = 'created'
            payload = Payload()
        else:
            action = 'modified'
            payload = await Payload.filter(pk=payload_id).first()

        payload.name = request.json['name']
        payload.notes = request.json['notes']
        await payload.save()

        if request.json['modules']:
            # Clear out any existing modules
            await Module.filter(payload=payload).delete()

            module_order = 1
            for payload_module in request.json['modules']:
                try:
                    if 'name' not in payload_module:
                        response = {'error': 'Module name must must be specified', action: False}
                        return json(response)
                    if not await ModuleLibrary.exists(name=payload_module['name']):
                        error_message = 'Module {name} doesn\'t exist in library'.format(id=payload_module['name'])
                        response = {'error': error_message, action: False}
                        return json(response)

                    module = Module()
                    module.name = payload_module['name']
                    module.payload = payload

                    module.order = module_order
                    module_order += 1
                    await module.save()

                    if 'options' in payload_module and 'values' in payload_module:
                        for index, option in enumerate(payload_module['values']):
                            module_option = ModuleOption()
                            module_option.module = module
                            module_option.name = option
                            module_option.value = payload_module['values'][option]

                            if payload_module['options'][index]['type'] == 'file':
                                module_option.is_file = True

                            await module_option.save()
                except Exception:
                    response = {'error': 'Unknown error occurred while adding module', action: False}
                    return json(response)

        response = {'id': payload.pk, 'error': '', action: True}
        return json(response)
    except IntegrityError:
        error_message = 'Payload name {name} already exists'.format(name=request.json['name'])
        response = {'error': error_message, action: False}
        return json(response)
    except Exception:
        response = {'error': 'Unknown error occurred while adding payload', action: False}
        return json(response)


async def get_module_from_library(module_library_id):
    module = await ModuleLibrary.filter(pk=module_library_id).first() \
        .values('name', 'description', 'author', 'supports_input')

    if module:
        module['options'] = await ModuleOptionLibrary.filter(module_id=module_library_id).all() \
            .values('name', 'description', 'type', 'required', 'default_value')
        return module
    else:
        return False


async def get_module_from_library_by_name(module_name):
    module = await ModuleLibrary.filter(name=module_name).first() \
        .values('id', 'name', 'description', 'author', 'supports_input')

    if module:
        module['options'] = await ModuleOptionLibrary.filter(module_id=module['id']).all() \
            .values('name', 'description', 'type', 'required', 'default_value')
        del module['id']
        return module
    else:
        return False


class PayloadsView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        if request.args.get('list'):
            all_payloads = await Payload.all().values('name', 'id')
        else:
            all_payloads = await Payload.all().values()
            for payload in all_payloads:
                payload['modules'] = await Module.filter(payload__id=payload['id']).all().values()

                for module in payload['modules']:
                    module_library = await get_module_from_library_by_name(module['name'])
                    if module_library:
                        module['supports_input'] = module_library['supports_input']
                        module['description'] = module_library['description']
        return json(all_payloads)

    async def post(self, request):
        return await payload_edit(request)


class PayloadView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, payload_id):
        payload = await Payload.filter(pk=payload_id).first().values()

        if payload:
            payload['modules'] = await Module.filter(payload__id=payload_id).all().values()
            for module in payload['modules']:
                module['collapsed'] = False

                module_library = await get_module_from_library_by_name(module['name'])
                if module_library:
                    module['supports_input'] = module_library['supports_input']
                    module['author'] = module_library['author']
                    module['description'] = module_library['description']

                    module['options'] = {}
                    module['options'] = module_library['options']

                    module['values'] = {}
                    for option in module_library['options']:
                        module_option = await ModuleOption.filter(module__id=module['id'],
                                                                  name=option['name']).first().values()
                        if module_option:
                            module['values'][option['name']] = module_option['value']
                        else:
                            module['values'][option['name']] = None
            return json(payload)
        else:
            response = {'error': 'Payload not found'}
            return json(response)

    async def put(self, request, payload_id):
        return await payload_edit(request, payload_id)

    async def delete(self, request, payload_id):
        payload = await Payload.filter(pk=payload_id).first()
        if payload:
            # Reset any paths to 404 that are serving this payload
            paths = await Path.filter(allow_action='payload').filter(payload_id=payload_id)
            for path in paths:
                path.payload_id = None
                path.allow_action = '404'
                await path.save()
            paths = await Path.filter(deny_action='payload').filter(deny_payload_id=payload_id)
            for path in paths:
                path.deny_payload_id = None
                path.deny_action = '404'
                await path.save()

            await payload.delete()
            response = {'id': payload.pk, 'deleted': True}
            return json(response)
        else:
            response = {'error': 'Payload not found', 'deleted': False}
            return json(response)


class PayloadGenerateView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, payload_id):
        try:
            payload_log_id = await generate_payload(payload_id, True)
            response = {'error': '', 'generated': True, 'payload_log_id': payload_log_id}
        except Exception as e:
            print("Error generating payload: " + str(e))
            response = {'error': 'Error generating payload', 'generated': False}
        return json(response)


class PayloadLogsView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request,payload_id):
        page = 1
        start = 0
        limit = 20

        if request.args.get('page'):
            page = int(request.args.get('page'))
            if page < 1:
                page = 1
        if request.args.get('limit'):
            limit = int(request.args.get('limit'))
            if limit < 1:
                limit = 1

        log_count = await PayloadLog.all().order_by('-datetime').count()
        number_of_pages = math.ceil(log_count / limit)
        start = (page - 1) * limit

        payload_log_results = await PayloadLog.filter(payload_id=payload_id).all().offset(start).limit(limit)\
                                               .order_by('-datetime')\
                                               .values('id', 'datetime', 'hash', 'manual', 'size')
        for payload_log in payload_log_results:
            if 'datetime' in payload_log:
                payload_log['datetime'] = payload_log['datetime'].isoformat()

        payload_log_response = {'results': payload_log_results,
                                'page_count': number_of_pages,
                                'results_count': log_count}
        return json(payload_log_response)


class PayloadLogView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, payload_id, log_id):
        payload_log = await PayloadLog.filter(id=log_id).all().first().values()
        if payload_log:
            if 'datetime' in payload_log:
                payload_log['datetime'] = payload_log['datetime'].isoformat()
            if 'output' in payload_log and payload_log['output'] is not None:
                decoded_output = payload_log['output'].decode(encoding="utf-8", errors="ignore")
                payload_log['output'] = decoded_output[:2048]
            return json(payload_log)
        else:
            response = {'error': 'Payload log not found'}
            return json(response)


class PayloadLogDownloadView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, payload_id, log_id):
        payload_log = await PayloadLog.filter(id=log_id).all().first().values('output')
        if payload_log:
            payload = await Payload.filter(id=payload_id).all().first().values('name')
            response = raw(payload_log['output'])
            response.headers.add("Content-Disposition", "attachment; filename={0}-{1};".format(payload['name'], log_id))
            return response
        else:
            response = {'error': 'Payload log not found'}
            return json(response)


class ModulesView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        all_modules = await Module.all().values()
        return json(all_modules)


class ModuleView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, module_id):
        module = await Module.filter(pk=module_id).first().values()
        if module:
            module_library = await get_module_from_library_by_name(module['name'])
            if module_library:
                module['options'] = {}
                module['options'] = module_library['options']

                module['values'] = {}
                for option in module_library['options']:
                    module_option = await ModuleOption.filter(module__id=module_id, name=option['name']).first().values()
                    if module_option:
                        module['values'][option['name']] = module_option['value']
                    else:
                        module['values'][option['name']] = None
                return json(module)
            else:
                response = {'error': 'Module not found in library'}
                return json(response)
        else:
            response = {'error': 'Module ID not found'}
            return json(response)

    # async def delete(self, request, module_id):
    #     module = await Module.filter(pk=module_id).first()
    #     if module:
    #         await module.delete()
    #         response = {'id': module.pk, 'deleted': True}
    #         return json(response)
    #     else:
    #         response = {'error': 'Module ID not found', 'deleted': False}
    #         return json(response)


class ModulesLibraryView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        if request.args.get('list'):
            all_modules = await ModuleLibrary.all().order_by('name').values('name', 'id')
        else:
            all_modules = await ModuleLibrary.all().order_by('name').values()
            for module in all_modules:
                module['options'] = await ModuleOptionLibrary.filter(module_id=module['id']).all() \
                    .values('name', 'description', 'type', 'required', 'default_value')

                module['values'] = {}
                for option in module['options']:
                    # Set the default values for fields in the front end
                    if option['type'] == 'file':
                        module['values'][option['name']] = ''
                    else:
                        module['values'][option['name']] = option['default_value']
        return json(all_modules)


class ModuleLibraryView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, module_library_id):
        module = await get_module_from_library(module_library_id)

        if module:
            module['values'] = {}
            for option in module['options']:
                # Set the default values for fields in the front end
                module['values'][option['name']] = option['default_value']
            return json(module)
        else:
            response = {'error': 'Module ID not found'}
            return json(response)
