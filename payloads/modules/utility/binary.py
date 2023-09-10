import base64
import binascii


def base64_decode(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    try:
        decoded = base64.b64decode(data)
        return decoded
    except binascii.Error:
        # If there's a decoding error return an empty string
        return b""


class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Returns static binary data.',
        }

        self.options = {
            'Bytes': {
                'Description': 'Bytes provided as a base64 string',
                'Required': True,
                'Type': 'text',
                'Value': ''
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        return base64_decode(self.options['Bytes']['Value'].encode('utf-8'))
