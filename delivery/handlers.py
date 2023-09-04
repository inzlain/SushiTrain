import asyncio
import ipaddress
import httpx
import geoip2.database
import geoip2.errors
import logging
import logging.handlers as handlers
import json
from sanic import Sanic
from os import getcwd, path as ospath
from jinja2 import Template
from delivery.models import RequestLog
from delivery.response import DeliveryHTTPResponse
from files.models import File
from payloads.generator import generate_payload
from payloads.models import Payload
from redirectors.models import Redirector, Path
from policies.models import GeographicRule, IPRangeRule, UserAgentRule, ASNRule

# Configure Maxmind Database
geoipdb_path = ospath.join(getcwd(), "./thirdparty/maxmind/GeoLite2-Country.mmdb")
try:
    geoip_reader = geoip2.database.Reader(geoipdb_path)
except FileNotFoundError:
    print("Could not locate GeoLite2-Country database!")
    geoip_reader = None
ipasndb_path = ospath.join(getcwd(), "./thirdparty/maxmind/GeoLite2-ASN.mmdb")
try:
    ipasn_reader = geoip2.database.Reader(ipasndb_path)
except FileNotFoundError:
    print("Could not locate GeoLite2-ASN database!")
    ipasn_reader = None

# Configure JSON request logger
log_format = "%(message)s"
request_json_logger = logging.getLogger(__name__)
request_json_logger.setLevel("INFO")
json_log_path = ospath.join(getcwd(), "./logs/requests.json")
file_handler = handlers.RotatingFileHandler(json_log_path, maxBytes=10485760, backupCount=10)
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)
request_json_logger.addHandler(file_handler)


async def log_to_json(request_log):
    json_log_line = {
        "log_id": request_log.pk,
        "allowed": request_log.allowed,
        "action": request_log.action,
        "datetime": request_log.datetime.isoformat(),
        "redirector": request_log.redirector_hostname,
        "path": request_log.redirector_path,
        "request_method": request_log.request_method,
        "request_ip": request_log.request_ip,
        "request_asn_org_name": request_log.request_asn_org_name,
        "request_country_code": request_log.request_country_code,
        "request_user_agent": request_log.request_user_agent,
        "request_hostname": request_log.request_hostname,
        "response_status": request_log.response_status,
        "response_size": len(request_log.response_body),
        "payload_id": request_log.payload_id,
        "file_id": request_log.file_id
    }

    request_json_logger.info(json.dumps(json_log_line))


async def slack_notify(path, request_log):
    management = Sanic.get_app("Management")
    template = Template(path.slack_template)
    message = template.render(path=request_log.redirector_path,
                              notes=path.notes,
                              redirector=request_log.redirector_hostname,
                              host_header=request_log.request_hostname,
                              method=request_log.request_method,
                              action=request_log.action,
                              allowed=request_log.allowed,
                              ip=request_log.request_ip,
                              asn=request_log.request_asn_org_name,
                              country=request_log.request_country_code,
                              user_agent=request_log.request_user_agent,
                              request_body=request_log.request_body,
                              request_headers=request_log.request_headers,
                              response_body=request_log.response_body,
                              response_headers=request_log.response_headers,
                              response_status=request_log.response_status,
                              ).encode('utf-8')
    r = httpx.post(management.config['SLACK_WEBHOOK_URL'],
                   content=message,
                   headers={"Content-type": "application/json"})


async def do_passthrough(request, request_log, response, url,
                         passthrough_request_headers,
                         passthrough_request_body,
                         passthrough_response_headers):
    try:
        passthrough_headers = {}
        passthrough_timeout = 5
        passthrough_body = b''
        if passthrough_request_body:
            passthrough_body = request.body

        if passthrough_request_headers:
            for header in request.headers:
                if header.lower() != 'x-redirector-hostname' and \
                        header.lower() != 'x-redirector-path' and \
                        header.lower() != 'x-forwarded-host' and \
                        header.lower() != 'x-forwarded-for' and \
                        header.lower() != 'host' and \
                        header.lower() != 'connection' and \
                        header.lower() != 'content-length':
                    passthrough_headers[header] = request.headers[header]

        async with httpx.AsyncClient() as client:
            passthrough = await client.request(method=request.method.upper(),
                                               url=url,
                                               content=passthrough_body,
                                               timeout=passthrough_timeout,
                                               headers=passthrough_headers,
                                               follow_redirects=True)

            response.body = passthrough.content
            request_log.response_body = passthrough.content

            response.status = passthrough.status_code
            request_log.response_status = passthrough.status_code

        if passthrough_response_headers:
            # Add the passthrough response headers
            for header in passthrough.headers:
                if header.lower() != 'connection' and \
                        header.lower() != 'content-encoding' and \
                        header.lower() != 'transfer-encoding' and \
                        header.lower() != 'content-length':
                    response.headers[header] = passthrough.headers[header]
                    request_log.response_headers += "{0}: {1}\n".format(header, passthrough.headers[header])


    except Exception as e:
        await request_log.add_message("Error retrieving retrieving passthrough URL -> Resonse will be empty")
        await request_log.add_message("Exception: {0}".format(str(e)))
        request_log.action = '200'
        response.body = ''
        request_log.response_body = b''
        response.status = 200
    return True


async def error(request, request_log, response, path):
    await request_log.add_message("Returning 404 not found response")
    request_log.action = '404'
    response.body = ''
    request_log.response_body = b''
    response.status = 404

    # Set the request to denied
    request_log.allowed = False
    request_log.response_status = response.status

    # Check if we need to send a notification
    if path:  # We can't send a notification on a request that didn't hit a configured path
        if path.slack_notifications:
            asyncio.create_task(slack_notify(path, request_log))

    # Save the request log and return the response
    # We don't check path logging settings here because we always want to log everything in an error case
    await request_log.save()
    await log_to_json(request_log)
    return response


async def allow(request, request_log, response, path):
    if path:
        if path.allow_action == '404':
            request_log.action = '404'
            response.body = b''
            request_log.response_body = b''
            response.status = 404
            await request_log.add_message("Response set to 404")
        elif path.allow_action == '302':
            request_log.action = '302'
            response.headers["Location"] = path.redirect_url
            request_log.response_headers += "{0}: {1}\n".format("Location", path.redirect_url)
            response.body = b''
            request_log.response_body = b''
            response.status = 302
            await request_log.add_message("Response set to 302: {0}".format(path.redirect_url))
        elif path.allow_action == 'payload':
            request_log.action = 'payload'
            payload = await Payload.filter(id=path.payload_id).first()
            request_log.payload_id = path.payload_id
            if payload:
                payload_output = await generate_payload(path.payload_id)
                response.body = payload_output
                request_log.response_body = payload_output
                await request_log.add_message("Response set to payload: {0}".format(payload.name))
            else:
                # No payloads exist on this path
                await request_log.add_message("Path has no payload configured -> [DENY]")
                return await deny(request, response, path)
        elif path.allow_action == 'file':
            request_log.action = 'file'
            file = await File.filter(id=path.file_id).first()
            request_log.file_id = path.file_id
            if file:
                response.body = file.bytes
                request_log.response_body = file.bytes
                await request_log.add_message("Response set to file: {0}".format(file.name))
            else:
                # No files exist on this path
                await request_log.add_message("Path has no file configured -> [DENY]")
                return await deny(request, response, path)
        elif path.allow_action == "passthrough":
            request_log.action = 'passthrough'
            if path.passthrough_url != '':
                await do_passthrough(request,
                                     request_log,
                                     response,
                                     path.passthrough_url,
                                     path.passthrough_request_headers,
                                     path.passthrough_request_body,
                                     path.passthrough_response_headers)
            else:
                # Empty passthrough URL configured
                await request_log.add_message("Path has no passthrough URL configured -> [DENY]")
                return await deny(request, response, path)
            await request_log.add_message("Response set to passthrough: {0}".format(path.passthrough_url))
        else:
            # Invalid allow action configured -> fallback to deny path
            await request_log.add_message("Invalid allow action configured on payload -> [DENY]")
            return await deny(request, request_log, response, path)

        # Add the allow headers
        for header in path.allow_headers:
            response.headers[header.header] = header.value
            request_log.response_headers += "{0}: {1}\n".format(header.header, header.value)

        # Check if need to wrap the output in a Jinja2 template
        if path.allow_template != '':
            template = Template(path.allow_template)
            rendered_template = template.render(output=response.body.decode(encoding="utf-8", errors="ignore")).encode(
                'utf-8')
            response.body = rendered_template
            request_log.response_body = rendered_template
            await request_log.add_message("Response wrapped in template")

        # Set the request to allowed
        request_log.allowed = True
        request_log.response_status = response.status

        # Check if we need to send a notification
        if path.slack_notifications:
            asyncio.create_task(slack_notify(path, request_log))

        # Save the request log and return the response
        await request_log.add_message("Returning ALLOW response")
        if path.logging_request_body is False:
            request_log.request_body = b''
        if path.logging_response_body is False:
            request_log.response_body = b''
        if path.logging is True:
            await request_log.save()
            await log_to_json(request_log)
        else:
            await request_log.delete()

        return response

    else:
        await request_log.add_message("Path doesn't exist -> [404]")
        return await error(request, request_log, response, None)


async def deny(request, request_log, response, path):
    if path:
        if path.deny_action == "404":
            request_log.action = '404'
            response.body = b''
            request_log.response_body = b''
            response.status = 404
            await request_log.add_message("Response set to 404")
        elif path.deny_action == '302':
            request_log.action = '302'
            response.headers["Location"] = path.deny_redirect_url
            request_log.response_headers += "{0}: {1}\n".format("Location", path.deny_redirect_url)
            response.body = b''
            request_log.response_body = b''
            response.status = 302
            await request_log.add_message("Response set to 302: {0}".format(path.deny_redirect_url))
        elif path.deny_action == "payload":
            request_log.action = 'payload'
            payload = await Payload.filter(id=path.deny_payload_id).first()
            request_log.payload_id = path.deny_payload_id
            if payload:
                payload_output = await generate_payload(path.deny_payload_id)
                response.body = payload_output
                request_log.response_body = payload_output
                await request_log.add_message("Response set to payload: {0}".format(payload.name))
            else:
                # No payloads exist on this path
                await request_log.add_message("Path has no deny payload configured -> [DENY]")
                return await deny(request, response, path)
        elif path.deny_action == "file":
            request_log.action = 'file'
            file = await File.filter(id=path.deny_file_id).first()
            request_log.file_id = path.deny_file_id
            if file:
                response.body = file.bytes
                request_log.response_body = file.bytes
                await request_log.add_message("Response set to file: {0}".format(file.name))
            else:
                # No files exist on this path
                await request_log.add_message("Path has no deny file configured -> [404]")
                return await error(request, request_log, response, path)
        elif path.deny_action == "passthrough":
            request_log.deny_action = 'passthrough'
            if path.deny_passthrough_url != '':
                await do_passthrough(request,
                                     request_log,
                                     response,
                                     path.deny_passthrough_url,
                                     path.deny_passthrough_request_headers,
                                     path.deny_passthrough_request_body,
                                     path.deny_passthrough_response_headers)
            else:
                # Empty passthrough URL configured
                await request_log.add_message("Path has no deny passthrough URL configured -> [DENY]")
                return await deny(request, response, path)
            await request_log.add_message("Response set to passthrough: {0}".format(path.deny_passthrough_url))
        else:
            request_log.action = '404'
            # Invalid deny action configured -> fallback to 404
            await request_log.add_message("Invalid deny action configured on payload -> [404]")
            return await error(request, request_log, response, path)

        # Add the deny headers
        for header in path.deny_headers:
            response.headers[header.header] = header.value
            request_log.response_headers += "{0}: {1}\n".format(header.header, header.value)

        # Check if need to wrap the output in a Jinja2 template
        if path.deny_template != '':
            template = Template(path.deny_template)
            rendered_template = template.render(output=response.body.decode(encoding="utf-8", errors="ignore")).encode(
                'utf-8')
            response.body = rendered_template
            request_log.response_body = rendered_template
            await request_log.add_message("Response wrapped in template")

        # Set the request to denied
        request_log.allowed = False
        request_log.response_status = response.status

        # Check if we need to send a notification
        if path.slack_notifications:
            asyncio.create_task(slack_notify(path, request_log))

        # Save the request log and return the response
        await request_log.add_message("Returning DENY response")
        if path.logging_request_body is False:
            request_log.request_body = b''
        if path.logging_response_body is False:
            request_log.response_body = b''
        if path.logging is True:
            await request_log.save()
            await log_to_json(request_log)
        else:
            await request_log.delete()
        return response

    else:
        await request_log.add_message("Path doesn't exist -> [404]")
        return await error(request, request_log, response, None)


async def http_request_handler(request):
    try:
        # Create a new request log and add the information that we know at this stage
        request_log = RequestLog()
        request_log.request_method = request.method
        request_log.request_body = request.body

        # Process the request headers
        request_headers = ''
        for request_header in request.headers:
            request_headers += '{0}: {1}\n'.format(request_header, request.headers[request_header])
        request_log.request_headers = request_headers

        if 'X-Forwarded-For' in request.headers:
            # Accepted practice is to put the original client IP address in the leftmost position
            # Truncate at 50 characters in case we get some really weird invalid value
            request_log.request_ip = request.headers['X-Forwarded-For'].split(',')[0][:50]

        if 'X-Forwarded-Host' in request.headers:
            request_log.request_hostname = request.headers['X-Forwarded-Host']

        if 'User-Agent' in request.headers:
            request_log.request_user_agent = request.headers['User-Agent']

        if 'X-Redirector-Hostname' in request.headers:
            request_log.redirector_hostname = request.headers['X-Redirector-Hostname']

        if 'X-Redirector-Path' in request.headers:
            request_log.redirector_path = request.headers['X-Redirector-Path']

        if request_log.request_ip != "":
            # Geolocate the IP address
            try:
                response = geoip_reader.country(request_log.request_ip)
                if not response.country.iso_code:
                    request_log.request_country_code = "??"
                else:
                    request_log.request_country_code = response.country.iso_code
            except geoip2.errors.GeoIP2Error:
                request_log.request_country_code = "??"
            except ValueError:
                request_log.request_country_code = "??"

            # Get the ASN Org Name
            try:
                response = ipasn_reader.asn(request_log.request_ip)
                if not response.autonomous_system_organization:
                    request_log.request_asn_org_name = "??"
                else:
                    request_log.request_asn_org_name = response.autonomous_system_organization
            except geoip2.errors.GeoIP2Error:
                request_log.request_asn_org_name = "??"
            except ValueError:
                request_log.request_country_code = "??"

        # Save the request log in case something goes wrong and so we can start logging messages against it
        await request_log.save()

        # Create a new response object
        response = DeliveryHTTPResponse()

        # Check if we have all four expected headers
        if 'X-Redirector-Hostname' not in request.headers:
            await request_log.add_message("Header safety check failed: X-Redirector-Hostname is not present -> [404]")
            return await error(request, request_log, response, None)
        if 'X-Redirector-Path' not in request.headers:
            await request_log.add_message("Header safety check failed: X-Redirector-Path is not present -> [404]")
            return await error(request, request_log, response, None)
        if 'X-Forwarded-Host' not in request.headers:
            await request_log.add_message("Header safety check failed: X-Forwarded-Host is not present -> [404]")
            return await error(request, request_log, response, None)
        if 'X-Forwarded-For' not in request.headers:
            await request_log.add_message("Header safety check failed: X-Forwarded-For is not present -> [404]")
            return await error(request, request_log, response, None)

        redirector = await Redirector.filter(hostname=request.headers['X-Redirector-Hostname']).first() \
            .prefetch_related('headers')
        if redirector:
            # Valid redirector hostname
            request_log.redirector = redirector

            # Add the redirector wide headers
            for header in redirector.headers:
                response.headers[header.header] = header.value
                request_log.response_headers += "{0}: {1}\n".format(header.header, header.value)

            path = await Path.filter(redirector_id=redirector.pk, path=request.headers['X-Redirector-Path']).first() \
                .prefetch_related('allow_headers', 'deny_headers')
            if path:
                request_log.path = path

                if path.enabled:
                    # Valid path
                    await request_log.add_message("Path is valid and enabled -> Policy check")

                    if path.policy:
                        # Check if the request country is on the blocklist
                        geographic_block_check = await GeographicRule.filter(policy_id=path.policy_id,
                                                                             allowlist=False,
                                                                             country_code=request_log.
                                                                             request_country_code.upper()
                                                                             ).all().count()
                        if geographic_block_check > 0:
                            await request_log.add_message("Country code {0} is on blocklist -> [DENY]"
                                                          .format(request_log.request_country_code))
                            return await deny(request, request_log, response, path)

                        # Check if any geographic allow rules are configured
                        geographic_allow_rules = await GeographicRule.filter(policy_id=path.policy_id,
                                                                             allowlist=True).all().count()
                        if geographic_allow_rules > 0:
                            # Check if the request country is on the allowlist
                            geographic_allow_check = await GeographicRule.filter(policy_id=path.policy_id,
                                                                                 allowlist=True,
                                                                                 country_code=request_log.
                                                                                 request_country_code.upper()
                                                                                 ).all().count()
                            if geographic_allow_check == 0:
                                await request_log.add_message("Country code {0} is not on allowlist -> [DENY]"
                                                              .format(request_log.request_country_code))
                                return await deny(request, request_log, response, path)

                        # Get all of the IP range block rules
                        ip_range_block_rules = await IPRangeRule.filter(policy_id=path.policy_id,
                                                                        allowlist=False).all()
                        # Check if the requesting IP is in any of the blocked ranges
                        ip_address = ipaddress.ip_address(request_log.request_ip)
                        for rule in ip_range_block_rules:
                            subnet = ipaddress.ip_network(rule.ip_range)
                            if ip_address in subnet:
                                await request_log.add_message("IP address {0} is on blocklist -> [DENY]"
                                                              .format(request_log.request_ip))
                                return await deny(request, request_log, response, path)

                        # Check if any IP range allow rules are configured
                        ip_range_allow_rules = await IPRangeRule.filter(policy_id=path.policy_id,
                                                                        allowlist=True).all()
                        if len(ip_range_allow_rules) > 0:
                            ip_allowed = False
                            # Check if the requesting IP is in any of the allowed ranges
                            for rule in ip_range_allow_rules:
                                subnet = ipaddress.ip_network(rule.ip_range)
                                if ip_address in subnet:
                                    ip_allowed = True
                                    break

                            if not ip_allowed:
                                await request_log.add_message("IP address {0} is not on allowlist -> [DENY]"
                                                              .format(request_log.request_ip))
                                return await deny(request, request_log, response, path)

                        # Check if the ASN is on the blocklist
                        asn_block_rules = await ASNRule.filter(policy_id=path.policy_id,
                                                               allowlist=False).all()
                        for rule in asn_block_rules:
                            if rule.asn_org_name.lower() in request_log.request_asn_org_name.lower():
                                await request_log.add_message("ASN Organization {0} is on blocklist -> [DENY]"
                                                              .format(request_log.request_asn_org_name))
                                return await deny(request, request_log, response, path)

                        # Check if any ASN allow rules are configured
                        asn_allow_rules = await ASNRule.filter(policy_id=path.policy_id,
                                                               allowlist=True).all()
                        if len(asn_allow_rules) > 0:
                            asn_allowed = False
                            # Check if the ASN matches any values on the allowlist
                            for rule in asn_allow_rules:
                                if rule.asn_org_name.lower() in request_log.request_asn_org_name.lower():
                                    asn_allowed = True
                                    break

                            if not asn_allowed:
                                if request_log.request_asn_org_name == "??":
                                    await request_log.add_message(
                                        "ASN Organization (unknown) is not on allowlist -> [DENY]")
                                else:
                                    await request_log.add_message("ASN Organization  {0} is not on allowlist -> [DENY]"
                                                                  .format(request_log.request_asn_org_name))
                                return await deny(request, request_log, response, path)

                        # Check if the user agent is on the blocklist
                        user_agent_block_rules = await UserAgentRule.filter(policy_id=path.policy_id,
                                                                            allowlist=False).all()
                        for rule in user_agent_block_rules:
                            if rule.user_agent.lower() in request_log.request_user_agent.lower():
                                await request_log.add_message("User agent {0} is on blocklist -> [DENY]"
                                                              .format(request_log.request_user_agent))
                                return await deny(request, request_log, response, path)

                        # Check if the user agent allow rules are configured
                        user_agent_allow_rules = await UserAgentRule.filter(policy_id=path.policy_id,
                                                                            allowlist=True).all()
                        if len(user_agent_allow_rules) > 0:
                            user_agent_allowed = False
                            # Check if the user agent matches any values on the allowlist
                            for rule in user_agent_allow_rules:
                                if rule.user_agent.lower() in request_log.request_user_agent.lower():
                                    user_agent_allowed = True
                                    break

                            if not user_agent_allowed:
                                if request_log.request_user_agent == "":
                                    await request_log.add_message("User agent (blank) is not on allowlist -> [DENY]"
                                                                  .format(request_log.request_user_agent))
                                else:
                                    await request_log.add_message("User agent {0} is not on allowlist -> [DENY]"
                                                                  .format(request_log.request_user_agent))
                                return await deny(request, request_log, response, path)

                        # We have successfully passed all of the policy checks
                        await request_log.add_message("Policy check passed -> [ALLOW]")
                        return await allow(request, request_log, response, path)
                    else:
                        await request_log.add_message("No policy configured -> [ALLOW]")
                        return await allow(request, request_log, response, path)
                else:
                    # Path is disabled so fallback to 404
                    await request_log.add_message("Path is disabled -> [404]")
                    return await error(request, request_log, response, path)
            else:
                # We have no path on this redirector, but the redirector does exist
                await request_log.add_message("Path is unknown -> [404]")
                return await error(request, request_log, response, None)
        else:
            # We have no redirector with this hostname
            await request_log.add_message("Redirector is unknown -> [404]")
            return await error(request, request_log, response, None)

    except Exception as e:
        # Catch all exception handler to return 404
        await request_log.add_message("Unexpected error occured -> [404]")
        await request_log.add_message("Exception: {0}".format(str(e)))
        print("UNKNOWN EXCEPTION: {0}".format(str(e)))
        return await error(request, request_log, response, None)
