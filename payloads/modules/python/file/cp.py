from payloads.modules.python.common import obfuscate_python_string


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Copies a file using shutil',
        }

        self.options = {
            'Source File': {
                'Description': 'The source file to copy',
                'Required': True,
                'Value': ''
            },
            'Destination File': {
                'Description': 'The destination file to copy to',
                'Required': True,
                'Value': ''
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        code = "import shutil;shutil.copy({0},{1});".format(obfuscate_python_string(self.options['Source File']['Value']),
                                                            obfuscate_python_string(self.options['Destination File']['Value']))
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)
        return code
