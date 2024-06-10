from payloads.helpers.string import random_string


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Returns a random string',
        }

        self.options = {
            'Characters': {
                'Description': 'Allowed characters in the random string',
                'Required': True,
                'Value': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            },
            'Minimum Length': {
                'Description': 'Minimum length of the random string',
                'Required': True,
                'Value': '5'
            },
            'Maximum Length': {
                'Description': 'Maximum length of the random string',
                'Required': True,
                'Value': '20'
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        if not isinstance(self.options['Minimum Length']['Value'], int):
            self.options['Minimum Length']['Value'] = 5
        if not isinstance(self.options['Maximum Length']['Value'], int):
            self.options['Maximum Length']['Value'] = 20

        return random_string(self.options['Minimum Length']['Value'],
                             self.options['Maximum Length']['Value'],
                             self.options['Characters']['Value'])
