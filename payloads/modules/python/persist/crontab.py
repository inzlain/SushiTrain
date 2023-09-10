from payloads.modules.python.persist.common import crontab_append


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Appends a command to the crontab',
        }

        self.options = {
            'Command': {
                'Description': 'The command to append to the crontab',
                'Required': True,
                'Value': ''
            },
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
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        code = crontab_append(self.options['Crontab Path']['Value'],
                              self.options['Schedule']['Value'],
                              self.options['Command']['Value'])
        return code
