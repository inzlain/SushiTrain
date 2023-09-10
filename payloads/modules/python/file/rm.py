from payloads.modules.python.common import obfuscate_python_string


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Deletes a file',
        }

        self.options = {
            'File': {
                'Description': 'The file to delete',
                'Required': True,
                'Value': ''
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        code = "import os;os.remove({0});".format(obfuscate_python_string(self.options['File']['Value']))
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)
        return code
