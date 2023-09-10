import zlib
from marshal import dumps
from payloads.helpers.string import random_string


class Module:

    def __init__(self, params=[]):
        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Converts Python code into compressed bytecode',
            'SupportsInput': True
        }

        self.options = {
        }

        self.previous_module_output = None

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value
            if option == 'PreviousModuleOutput':
                self.previous_module_output = value

    def generate(self):
        var_exec = random_string(10, 20)
        bytecode = dumps(compile(self.previous_module_output, random_string(10, 20), "exec"))
        compressed_bytecode = zlib.compress(bytecode)

        code = "import zlib;from marshal import loads;"
        code += "{0}=exec;".format(var_exec)  # Alias exec function
        code += "{0}(loads(zlib.decompress({1})));".format(var_exec, compressed_bytecode)
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)

        return code
