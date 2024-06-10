from payloads.helpers.string import random_string


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Finds a given string in the input and replaces it with a random string',
            'SupportsInput': True
        }

        self.options = {
            'Find': {
                'Description': 'The case-sensitive text string to find and replace',
                'Required': True,
                'Value': 'CHANGE_ME'
            },
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

        self.previous_module_output = None

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value
            if option == 'PreviousModuleOutput':
                self.previous_module_output = value

    def generate(self):
        if not isinstance(self.options['Minimum Length']['Value'], int):
            self.options['Minimum Length']['Value'] = 5
        if not isinstance(self.options['Maximum Length']['Value'], int):
            self.options['Maximum Length']['Value'] = 20

        replacement_string = random_string(self.options['Minimum Length']['Value'],
                                           self.options['Maximum Length']['Value'],
                                           self.options['Characters']['Value'])

        return self.previous_module_output.decode(encoding="utf-8", errors="ignore") \
            .replace(self.options['Find']['Value'], replacement_string)
