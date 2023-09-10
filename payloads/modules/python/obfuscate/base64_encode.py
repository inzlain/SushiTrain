import base64
from payloads.helpers.string import random_string


class Module:

    def __init__(self, params=[]):
        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Converts Python code into a base64 string',
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
        base64_string = base64.b64encode(self.previous_module_output).strip()

        code = "import base64;"
        code += "{0}=exec;".format(var_exec)  # Alias exec function
        code += "{0}(base64.b64decode({1}))".format(var_exec, base64_string)
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)
        return code
