from payloads.helpers.string import random_string


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Finds a given string in the input and replaces it with another string',
            'SupportsInput': True
        }

        self.options = {
            'Find': {
                'Description': 'The case-sensitive text string to find and replace',
                'Required': True,
                'Value': 'CHANGE_ME'
            },
            'Replace': {
                'Description': 'Allowed characters in the random string',
                'Required': True,
                'Value': 'NEW_VALUE'
            }
        }

        self.previous_module_output = None

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value
            if option == 'PreviousModuleOutput':
                self.previous_module_output = value

    def generate(self):
        return self.previous_module_output.decode(encoding="utf-8", errors="ignore") \
            .replace(self.options['Find']['Value'], self.options['Replace']['Value'])
