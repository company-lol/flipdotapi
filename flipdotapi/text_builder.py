from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap 
import os
import logging
from flipdotapi.fonts import fonts as fonts

f = fonts()
FONTS =  f.get_fonts()

class TextBuilder(object):

    LOG_LEVEL = logging.DEBUG

    """Helper class for converting text to images

    Attributes:
        height (int): Height of the image
        width (int): Width of the image
    """
    

    def __init__(self, width: int, height: int):
        """Constructor for a TextHelper object

        Args:
            width (int): Width of the output text images
            height (int): Height of the output text images
        """
        self.width = width
        self.height = height
        logging.basicConfig(level=self.LOG_LEVEL)
        self.logger = logging.getLogger(__name__)
      
    def fitfont(self, txt, font):
        font_file_name = FONTS[font].path
        img_fraction = 1 
        fontsize = 6
        font = ImageFont.truetype(font_file_name, fontsize)
        while font.getsize(txt)[0] < img_fraction * self.width:
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            font = ImageFont.truetype(font_file_name, fontsize)

        while font.getsize(txt)[1] > self.height:
            
            # iterate until the text size is just larger than the criteria
            fontsize -= 1
            font = ImageFont.truetype(font_file_name, fontsize)

        # optionally de-increment to be sure it is less than criteria
        #fontsize -= 1
        font = ImageFont.truetype(font_file_name, fontsize)
        size, (_, offset_y) = font.font.getsize(txt)
        self.logger.debug("Font size: " + str(size))
        self.logger.debug("Fontsize: " + str(fontsize))
        return font

    def text_image(
            self,
            text: str,
            font_name: str="nintendo-entertainment-system-regular",
            alignment='left',
            fit=True):
        """Creates an image from text

        Args:
            text (str): Text to convert to an image
            font_name (str): Font name to use to render the image
            alignment (str, optional): Alignment ('left', 'right' or 'centre')

        Returns:
            TYPE: Image data
        """

        # Get some details about the font
        font = self._get_font(font_name)
       

        if fit:
            wrapper = textwrap.TextWrapper(width=12) 
            lines = wrapper.wrap(text=text)
        else:
            lines = self._get_lines(text, font)

        images = []
        for line in lines:
            if fit:
                font = self.fitfont(line, font_name)
            size, (_, offset_y) = font.font.getsize(line)
            self.logger.debug("Final Fontsize: " + str(size))
            # Determine Text starting position
            text_position = self._get_text_position(size, alignment)
            text_position['y'] -= offset_y

            # Create a new image
            image = Image.new(
                mode='L', size=(self.width, self.height), color=0)
            # Get a drawing context
            draw = ImageDraw.Draw(image)

            # Draw text
            draw.text(
                (text_position['x'], text_position['y']),
                line,
                fill=1,
                font=font)
            images.append(np.array(image))

        return images
    
    

    def _get_lines(self, text, font):
        # Assert that the font is appropriate
        (_, height), (_, _) = font.font.getsize(text)
        if height > self.height:
            raise RuntimeError("Font too tall for {}x{} image (is {})".format(
                self.width, self.height, height))

        # Convert the text into multiple lines
        lines = []
        while text:
            line, text = self._get_line(text, font, self.width)
            lines.append(line)
        return lines

    @staticmethod
    def _get_line(text, font, total_width):
        # First check if text fits on one line
        text = text.strip()
        (width, _), (_, _) = font.font.getsize(text)

        if width <= total_width:
            # All the text fits on one line
            return text, ""

        def words_to_line(words):
            return ' '.join(words)

        all_words = text.split()
        previous_line = None
        for i, word in enumerate(all_words):
            # Create a new line with 'i' words
            query_line = words_to_line(all_words[:(i + 1)])
            (width, _), _ = font.font.getsize(query_line)

            # Check if line is too long
            if width > total_width:
                if i == 0:
                    raise RuntimeError(
                        "'{}' is too long to fit image (is {} expected less than {}) ".format(word, width, total_width))

                # We have found the word that makes the line too long
                text = text[len(previous_line):].strip()
                return previous_line, text

            # Iterate
            previous_line = query_line

        assert False

    def _get_text_position(self, size, alignment: str):
        """Determines the top-left position for the text sub-image

        Args:
            size (int): Size
            alignment (str): Text alignment ('left', 'right' or 'centre')

        Returns:
            dict: (x, y) position

        Raises:
            ValueError: Invalid alignment argument
        """
        width, height = size

        if width > self.width:
            print((
                "Warning: {}x{} text will be clipped "
                "to fit on {}x{} image").format(
                    width, height, self.width, self.height))

        text_position = {
            'y': 0
        }

        # Find x-position based on alignment
        if alignment == 'left':
            text_position['x'] = 0
        elif alignment == 'right':
            text_position['x'] = self.width - width
        elif alignment == 'centre':
            text_position['x'] = int(round((self.width - width) / 2))
        else:
            raise ValueError("Invalid alignment '{}'".format(alignment))

        return text_position

    @staticmethod
    def _get_font( font: str, points=None):
        # Get a font and its height

        font_details = FONTS[font]
        if not points:
            font_size = int(font_details.points / 3 * 4)
             
        else:
            font_size = int(points / 3 * 4)
            
        font = ImageFont.truetype( font_details.path, font_size )

        return font
