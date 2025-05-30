from payloads.helpers.bytes import random_bytes


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Returns random binary bytes',
        }

        self.options = {
            'Minimum Length': {
                'Description': 'Minimum length of the random bytes',
                'Required': True,
                'Value': '5'
            },
            'Maximum Length': {
                'Description': 'Maximum length of the random bytes',
                'Required': True,
                'Value': '20'
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        try:
            self.options['Minimum Length']['Value'] = int(self.options['Minimum Length']['Value'])
        except ValueError:
            self.options['Minimum Length']['Value'] = 5

        try:
            self.options['Maximum Length']['Value'] = int(self.options['Maximum Length']['Value'])
        except ValueError:
            self.options['Maximum Length']['Value'] = 20

        return random_bytes(self.options['Minimum Length']['Value'], self.options['Maximum Length']['Value'])
