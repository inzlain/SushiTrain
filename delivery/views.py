import csv
import io
import math

from sanic import text
from sanic.response import json, raw
from sanic.views import HTTPMethodView
from sanic_jwt.decorators import protected
from tortoise.expressions import Q, F
from tortoise.functions import Count
from delivery.models import RequestLog, RequestLogMessage
from payloads.models import Payload
from files.models import File


class RequestLogsView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        page = 1
        start = 0
        limit = 20
        query = ''

        export_rows = 1000

        if request.args.get('page'):
            page = int(request.args.get('page'))
            if page < 1:
                page = 1
        if request.args.get('limit'):
            limit = int(request.args.get('limit'))
            if limit < 1:
                limit = 1
        if request.args.get('query'):
            query = request.args.get('query')

        if query == '':
            log_count = await RequestLog.all().order_by('-datetime').count()
            number_of_pages = math.ceil(log_count / limit)
            start = (page - 1) * limit

            request_log_results = await RequestLog.all().offset(start).limit(limit).order_by('-datetime')\
                .values('id', 'datetime', 'allowed', 'redirector_hostname', 'redirector_path', 'request_ip',
                        'request_asn_org_name', 'request_country_code', 'request_user_agent', 'request_hostname')
            for request_log in request_log_results:
                if 'datetime' in request_log:
                    request_log['datetime'] = request_log['datetime'].isoformat()
        else:
            log_count = await RequestLog.all().filter(
                Q(redirector_hostname__icontains=query) |
                Q(redirector_path__icontains=query) |
                Q(request_hostname__icontains=query) |
                Q(request_user_agent__icontains=query) |
                Q(request_asn_org_name__icontains=query) |
                Q(request_ip__icontains=query)
            ).order_by('-datetime').count()

            number_of_pages = math.ceil(log_count / limit)
            start = (page - 1) * limit

            request_log_results = await RequestLog.all().filter(
                Q(redirector_hostname__icontains=query) |
                Q(redirector_path__icontains=query) |
                Q(request_hostname__icontains=query) |
                Q(request_user_agent__icontains=query) |
                Q(request_asn_org_name__icontains=query) |
                Q(request_ip__icontains=query)
            ).offset(start).limit(limit).order_by('-datetime') \
                .values('id', 'datetime', 'allowed', 'redirector_hostname', 'redirector_path', 'request_ip',
                        'request_asn_org_name', 'request_country_code', 'request_user_agent', 'request_hostname')
            for request_log in request_log_results:
                if 'datetime' in request_log:
                    request_log['datetime'] = request_log['datetime'].isoformat()

        if request.args.get('export'):
            csv_output = io.StringIO()
            csv_writer = csv.writer(csv_output)
            csv_writer.writerow(['id', 'datetime', 'allowed', 'hostname', 'path', 'ip', 'asn', 'country', 'user-agent', 'host_header'])

            for request_log in request_log_results:
                csv_writer.writerow([request_log['id'],
                                     request_log['datetime'],
                                     request_log['allowed'],
                                     request_log['redirector_hostname'],
                                     request_log['redirector_path'],
                                     request_log['request_ip'],
                                     request_log['request_asn_org_name'],
                                     request_log['request_country_code'],
                                     request_log['request_user_agent'],
                                     request_log['request_hostname']])


            response = text(csv_output.getvalue())
            response.headers.add('Content-Type', "text/csv")
            response.headers.add("Content-Disposition", "attachment; filename=request-log-export.csv;")

            return response

        request_log_response = {'results': request_log_results,
                                'page_count': number_of_pages,
                                'results_count': log_count}
        return json(request_log_response)


class RequestLogView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, request_id):
        request_log = await RequestLog.filter(id=request_id).first().values()
        if request_log:
            if 'datetime' in request_log:
                request_log['datetime'] = request_log['datetime'].isoformat()
            if 'payload_id' in request_log:
                payload = await Payload.filter(id=request_log['payload_id']).all().first().values('name')
                if payload:
                    request_log['payload_name'] = payload['name']
            if 'file_id' in request_log:
                file = await File.filter(id=request_log['file_id']).all().first().values('name')
                if file:
                    request_log['file_name'] = file['name']
            if 'request_body' in request_log and request_log['request_body'] is not None:
                decoded_body = request_log['request_body'].decode(encoding="utf-8", errors="ignore")
                request_log['request_body'] = decoded_body[:2048]
            if 'response_body' in request_log and request_log['response_body'] is not None:
                decoded_body = request_log['response_body'].decode(encoding="utf-8", errors="ignore")
                request_log['response_body'] = decoded_body[:2048]

            request_log['messages'] = await RequestLogMessage.filter(request_log__id=request_id).all().values('datetime', 'message')
            for message in request_log['messages']:
                if 'datetime' in message:
                    message['datetime'] = message['datetime'].isoformat()

            return json(request_log)
        else:
            response = {'error': 'Request log not found'}
            return json(response)


class RequestLogDownloadView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request, request_id, download_type):
        request_log = await RequestLog.filter(id=request_id).first().values()
        if request_log:
            if download_type == 'request':
                response = raw(request_log['request_body'])
                response.headers.add("Content-Disposition", "attachment; filename=request-body-{0};".format(request_id))
                return response
            if download_type == 'response':
                response = raw(request_log['response_body'])
                response.headers.add("Content-Disposition", "attachment; filename=response-body-{0};".format(request_id))
                return response
        else:
            response = {'error': 'Request log not found'}
            return json(response)


class MonitorView(HTTPMethodView):
    decorators = [protected()]

    async def get(self, request):
        allowed_requests = await RequestLog.filter(allowed=True).all().order_by('-datetime').limit(5) \
            .values('id', 'datetime', 'redirector_hostname', 'redirector_path', 'request_ip',
                    'request_asn_org_name', 'request_country_code', 'request_user_agent', 'request_hostname')
        for request in allowed_requests:
            if 'datetime' in request:
                request['datetime'] = request['datetime'].isoformat()

        denied_requests = await RequestLog.filter(allowed=False).all().order_by('-datetime').limit(5) \
            .values('id', 'datetime', 'redirector_hostname', 'redirector_path', 'request_ip',
                    'request_asn_org_name', 'request_country_code', 'request_user_agent', 'request_hostname')
        for request in denied_requests:
            if 'datetime' in request:
                request['datetime'] = request['datetime'].isoformat()

       # allowed_visitors = await RequestLog.filter(allowed=True).annotate(count=Count('request_ip', distinct=True)).all().values('request_ip', 'count')


        response = {'allowed_requests': allowed_requests,
                    'denied_requests': denied_requests,
                    'allowed_visitors': [],
                    'denied_visitors': []}
        return json(response)