class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Returns a static file',
        }

        self.options = {
            'File': {
                'Description': 'A static file',
                'Required': True,
                'Type': 'file',
                'Value': ''
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        return self.options['File']['Value']
