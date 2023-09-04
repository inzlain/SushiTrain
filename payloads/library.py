from payloads.models import ModuleLibrary, ModuleOptionLibrary
import fnmatch
import os
import importlib
import subprocess


async def refresh_module_library():
    modules_path = os.path.join(os.getcwd(), 'payloads/modules/')
    print("Loading modules from {0}".format(modules_path))

    # Clear out the existing module information in the library
    await ModuleLibrary.all().delete()
    await ModuleOptionLibrary.all().delete()  # There shouldn't be any orphaned module options but just in case

    for root, dirs, files in os.walk(modules_path):
        # Install any Python requirements as we go
        for filename in fnmatch.filter(files, 'requirements.txt'):
            try:
                subprocess.call(['pip3', 'install', '-r', os.path.join(root, filename)])
            except Exception as e:
                print("Error installing requirements.txt {0} - Exception: {1}".format(os.path.join(root, filename), str(e)))
            continue

        # Load the modules
        for filename in fnmatch.filter(files, '*.py'):
            try:
                if filename != '__init__.py':
                    new_module = ModuleLibrary()

                    module_path = os.path.join(root, filename[0:-3]) \
                        .replace(modules_path, '') \
                        .replace('/', '.')

                    new_module.name = module_path
                    import_path = 'payloads.modules.' + module_path

                    imported_module = importlib.import_module(import_path)
                    module_instance = getattr(imported_module, 'Module')
                    module_info = module_instance([]).info
                    module_options = module_instance([]).options

                    if 'Author' in module_info:
                        new_module.author = module_info['Author']
                    if 'Description' in module_info:
                        new_module.description = module_info['Description']
                    if 'SupportsInput' in module_info:
                        new_module.supports_input = module_info['SupportsInput']
                    await new_module.save()

                    for module_option in module_options:
                        new_module_option = ModuleOptionLibrary()
                        new_module_option.module = new_module
                        new_module_option.name = module_option

                        if 'Description' in module_options[module_option]:
                            new_module_option.description = module_options[module_option]['Description']
                        if 'Type' in module_options[module_option]:
                            new_module_option.type = module_options[module_option]['Type']
                        if 'Required' in module_options[module_option]:
                            new_module_option.required = module_options[module_option]['Required']
                        if 'Value' in module_options[module_option]:
                            new_module_option.default_value = module_options[module_option]['Value']
                        await new_module_option.save()

            except Exception as e:
                print("Error loading module {0} - Exception: {1}".format(filename, str(e)))
                continue

    print("Successfully loaded {0} modules!".format(await ModuleLibrary.all().count()))


