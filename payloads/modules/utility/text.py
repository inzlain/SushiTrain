class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Returns a static text string',
        }

        self.options = {
            'Text': {
                'Description': 'A static text string',
                'Required': True,
                'Value': 'example'
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        return self.options['Text']['Value']
