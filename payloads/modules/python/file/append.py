from payloads.helpers.string import random_string
from payloads.modules.python.common import obfuscate_python_string


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Appends a line to a file',
        }

        self.options = {
            'Line': {
                'Description': 'The line to append',
                'Required': True,
                'Value': ''
            },
            'File': {
                'Description': 'The target file to modify',
                'Required': True,
                'Value': ''
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        var_file = random_string(length_minimum=10, length_maximum=20)

        code = "import os;"
        code += "{0}=open(os.path.expanduser({1}),'a');".format(var_file,
                                                                obfuscate_python_string(self.options['File']['Value']))
        code += "{0}.write({1});".format(var_file, obfuscate_python_string(self.options['Line']['Value']) + "\n")
        code += "{0}.close();".format(var_file)
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)
        return code
