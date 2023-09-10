from payloads.modules.python.common import obfuscate_python_string


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Copies a directory using shutil',
        }

        self.options = {
            'Source Directory': {
                'Description': 'The source directory to copy',
                'Required': True,
                'Value': ''
            },
            'Destination Directory': {
                'Description': 'The destination directory to copy to',
                'Required': True,
                'Value': ''
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        code = "import shutil;shutil.copytree({0},{1});".format(obfuscate_python_string(self.options['Source Directory']['Value']),
                                                                obfuscate_python_string(self.options['Destination Directory']['Value']))
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)
        return code
