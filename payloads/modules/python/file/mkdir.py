from payloads.modules.python.common import obfuscate_python_string


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Creates a directory',
        }

        self.options = {
            'Directory': {
                'Description': 'The directory to create',
                'Required': True,
                'Value': ''
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        code = "import os;os.mkdir({0});".format(obfuscate_python_string(self.options['Directory']['Value']))
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)
        return code
