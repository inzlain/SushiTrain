import zlib
from payloads.helpers.string import random_string


class Module:

    def __init__(self, params=[]):
        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Compresses Python code with zlib into bytes',
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
        compressed_data = zlib.compress(self.previous_module_output)

        code = "import zlib;"
        code += "{0}=exec;".format(var_exec)  # Alias exec function
        code += "{0}(zlib.decompress({1}));".format(var_exec, compressed_data)
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)

        return code
