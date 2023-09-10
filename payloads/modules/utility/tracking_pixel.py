from io import BytesIO
from random import randint
from PIL import Image

class Module:

    def __init__(self, params=[]):

        self.info = {
            'Author': 'Alain Homewood',
            'Description': 'Generates randomly generated PNG image for use as a tracking pixel',
        }

        self.options = {
            'Width': {
                'Description': 'Image width in pixels',
                'Required': False,
                'Type': 'text',
                'Value': '1'
            },
            'Height': {
                'Description': 'Image height in pixels',
                'Required': False,
                'Type': 'text',
                'Value': '1'
            },
        }

        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):
        try:
            width = int(self.options['Width']['Value'])
            height = int(self.options['Height']['Value'])
        except ValueError:
            width = 1
            height = 1

        png_byte_buffer = BytesIO()
        png = Image.new('RGBA', (width, height), (randint(0, 255), randint(0, 255), randint(0, 255), 0))
        png.save(png_byte_buffer, format='PNG')

        return png_byte_buffer.getvalue()
