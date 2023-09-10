import base64


class Module:

    def __init__(self, params=[]):
        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Performs base64 encoding of input data',
            'SupportsInput': True
        }

        self.options = {
        }

        self.previous_module_output = None

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value
            if option == 'PreviousModuleOutput':
                self.previous_module_output = value

    def generate(self):
        return base64.b64encode(self.previous_module_output).strip()
