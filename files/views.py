from sanic.response import json, raw
from sanic.views import HTTPMethodView
from sanic_jwt.decorators import protected
from hashlib import sha256
from files.models import File
from payloads.models import ModuleOption
from redirectors.models import Path


class FilesView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        all_files = await File.all().order_by('name').values('id', 'name', 'size', 'hash')
        return json(all_files)

    async def post(self, request):
        if not request.files:
            response = {'error': 'No files provided', 'uploaded': False}
            return json(response)

        try:
            uploaded_file = request.files.get('file')

            # Check if the filename already exits, otherwise create a new one
            file = await File.filter(name=uploaded_file.name).first()
            if not file:
                file = File()

            file.name = uploaded_file.name
            file.bytes = uploaded_file.body
            file.size = len(file.bytes)

            hasher = sha256()
            hasher.update(uploaded_file.body)
            file.hash = hasher.hexdigest()

            await file.save()

            response = {'id': file.pk, 'uploaded': True}
            return json(response)
        except Exception:
            response = {'error': 'Unknown error occured during file upload', 'uploaded': False}
            return json(response)


class FileView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, file_id):
        file = await File.filter(pk=file_id).first()
        if file:
            response = raw(file.bytes)
            response.headers.add("Content-Disposition", "attachment; filename={0};".format(file.name))
            return response
        else:
            response = {'error': 'File ID not found'}
            return json(response)

    async def delete(self, request, file_id):
        file = await File.filter(pk=file_id).first()
        if file:
            # Reset values for any modules that are using this file
            module_options = await ModuleOption.filter(is_file=True).filter(value=file_id)
            for option in module_options:
                option.value = ''
                await option.save()

            # Reset any paths to 404 that are serving this file
            paths = await Path.filter(allow_action='file').filter(file_id=file_id)
            for path in paths:
                path.file_id = None
                path.allow_action = '404'
                await path.save()
            paths = await Path.filter(deny_action='file').filter(deny_file_id=file_id)
            for path in paths:
                path.deny_file_id = None
                path.deny_action = '404'
                await path.save()

            # Finally delete the file itself
            await file.delete()

            response = {'id': file.pk, 'deleted': True}
            return json(response)
        else:
            response = {'error': 'File ID not found', 'deleted': False}
            return json(response)
