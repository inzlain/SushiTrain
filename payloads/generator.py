import importlib
from hashlib import sha256

from files.models import File
from payloads.models import Payload, PayloadLog


async def generate_payload(payload_id, manual_trigger=False):
    payload = await Payload.filter(id=payload_id).first().prefetch_related('modules', 'modules__options')
    payload_output = b''
    log = ''

    if payload:
        payload_log = PayloadLog()
        payload_log.payload = payload
        if manual_trigger:
            payload_log.manual = True

        if payload.modules:
            for module in payload.modules:
                log += "Executing module: {0}\n".format(module.name)

                module_options = []
                for option in module.options:
                    if option.is_file:
                        if option.value != '':
                            file = await File.filter(id=option.value).first()
                            module_options.append([option.name, file.bytes])
                            log += " - {0}: {1} ({2})\n".format(option.name, file.name, file.hash)
                        else:
                            module_options.append([option.name, ''])
                            log += " - {0}: <no file configured>\n".format(option.name)
                    else:
                        module_options.append([option.name, option.value])
                        log += " - {0}: {1}\n".format(option.name, option.value)

                import_path = 'payloads.modules.' + module.name
                imported_module = importlib.import_module(import_path)
                module_instance = getattr(imported_module, 'Module')

                # Check if the module supports taking input from the previous modules
                module_supports_input = False
                module_info = module_instance([]).info
                if 'SupportsInput' in module_info:
                    if module_info['SupportsInput'] is True:
                        module_supports_input = True
                        module_options.append(['PreviousModuleOutput', payload_output])
                        log += " - Module supports input\n"

                # Add a reference to the module and payload IDs for modules that want to do reflection
                # module_options.append(['ModuleID', module.pk])
                # module_options.append(['PayloadID', payload_id])

                module_output = module_instance(module_options).generate()

                # If we got text output instead of bytes then assume it's utf-8 encoded
                if type(module_output) != bytes:
                    module_output = bytes(module_output, 'utf-8')

                if module_supports_input is True:
                    # replace the previous module output
                    payload_output = module_output
                else:
                    # append to the previous module output
                    payload_output += module_output
        else:
            log += "No modules configured! Payload output will be blank!\n"

        log += "\nPayload generated successfully!\n"
        payload_log.log = log

        payload_log.output = payload_output
        payload_log.size = len(payload_output)

        hasher = sha256()
        hasher.update(payload_output)
        payload_log.hash = hasher.hexdigest()

        await payload_log.save()

        if manual_trigger:
            return payload_log.pk

    else:
        # This should probably log to an error log or link it to request log?
        print("Something went wrong when trying to a find a payload!")

    return payload_output


