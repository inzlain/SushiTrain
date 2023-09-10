class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Performs a redirection to a URL via an HTML meta refresh',
        }

        self.options = {
            'Location': {
                'Description': 'The URL to redirect the visitor to',
                'Required': True,
                'Type': 'url',
                'Value': 'https://www.example.com/'
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        html = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0;url=Location" />
    <title></title>
</head>
    <body>
    </body>
</html>"""
        html = html.replace("Location", self.options['Location']['Value'])
        return html
