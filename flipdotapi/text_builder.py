from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap
import os
import logging
from flipdotapi.fonts import fonts as fonts

f = fonts()
FONTS = f.get_fonts()

class TextBuilder(object):
    LOG_LEVEL = logging.DEBUG

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.scroll = True
        logging.basicConfig(level=self.LOG_LEVEL)
        self.logger = logging.getLogger(__name__)

    def fitfont(self, txt, font):
        font_file_name = FONTS[font].path
        img_fraction = 1
        fontsize = 6
        font = ImageFont.truetype(font_file_name, fontsize)
        while font.getbbox(txt)[2] < img_fraction * self.width:
            fontsize += 1
            font = ImageFont.truetype(font_file_name, fontsize)

        while font.getbbox(txt)[3] > self.height:
            fontsize -= 1
            font = ImageFont.truetype(font_file_name, fontsize)

        font = ImageFont.truetype(font_file_name, fontsize)
        bbox = font.getbbox(txt)
        self.logger.debug(f"Font size: {bbox}")
        self.logger.debug(f"Fontsize: {fontsize}")
        return font

    def text_image(self, text: str, font_name: str="nintendo-entertainment-system-regular", alignment='left', fit=True, scroll=True, scroll_speed=25):
        if scroll:
            return self.text_image_scroll(text=text, font_name=font_name, scroll_speed=scroll_speed)
        else:
            return self.text_image_lines(text=text, font_name=font_name, alignment=alignment, fit=fit)

    def text_image_scroll(self, text: str, font_name: str="nintendo-entertainment-system-regular", scroll_speed: int=25):
        font_path = FONTS[font_name].path
        font = ImageFont.truetype(font_path, 15)
        bbox = font.getbbox(text)
        size = (bbox[2], bbox[3])

        image = Image.new('L', size=size)
        draw = ImageDraw.Draw(image)
        draw.fontmode = "1"
        draw.text((0,0), text, font=font, fill=1)
        steps = round(size[0]/scroll_speed)

        images = []
        for i in range(steps):
            buffer = (scroll_speed*i)
            width = buffer
            width_2 = self.width + buffer
            crop = (width,0,width_2,self.height)
            part = image.crop(crop)
            images.append(np.array(part))
        return images

    def text_image_lines(self, text: str, font_name: str="nintendo-entertainment-system-regular", alignment='left', fit=True):
        font = self._get_font(font_name)
        images = []

        if fit:
            wrapper = textwrap.TextWrapper(width=12)
            lines = wrapper.wrap(text=text)
        else:
            lines = self._get_lines(text, font)

        for line in lines:
            if fit:
                font = self.fitfont(line, font_name)
            bbox = font.getbbox(line)
            size = (bbox[2], bbox[3])
            text_position = self._get_text_position(size, alignment)
            text_position['y'] -= bbox[1]

            image = Image.new(mode='L', size=(self.width, self.height), color=0)
            draw = ImageDraw.Draw(image)
            draw.text((text_position['x'], text_position['y']), line, fill=1, font=font)
            images.append(np.array(image))

        return images

    def _get_lines(self, text, font):
        bbox = font.getbbox(text)
        if bbox[3] > self.height:
            raise RuntimeError(f"Font too tall for {self.width}x{self.height} image (is {bbox[3]})")

        lines = []
        while text:
            line, text = self._get_line(text, font, self.width)
            lines.append(line)
        return lines

    @staticmethod
    def _get_line(text, font, total_width):
        text = text.strip()
        bbox = font.getbbox(text)

        if bbox[2] <= total_width:
            return text, ""

        def words_to_line(words):
            return ' '.join(words)

        all_words = text.split()
        previous_line = None
        for i, word in enumerate(all_words):
            query_line = words_to_line(all_words[:(i + 1)])
            bbox = font.getbbox(query_line)

            if bbox[2] > total_width:
                if i == 0:
                    raise RuntimeError(f"'{word}' is too long to fit image (is {bbox[2]} expected less than {total_width})")

                text = text[len(previous_line):].strip()
                return previous_line, text

            previous_line = query_line

        assert False

    def _get_text_position(self, size, alignment: str):
        width, height = size

        if width > self.width:
            print(f"Warning: {width}x{height} text will be clipped to fit on {self.width}x{self.height} image")

        text_position = {'y': 0}

        if alignment == 'left':
            text_position['x'] = 0
        elif alignment == 'right':
            text_position['x'] = self.width - width
        elif alignment == 'centre':
            text_position['x'] = int(round((self.width - width) / 2))
        else:
            raise ValueError(f"Invalid alignment '{alignment}'")

        return text_position

    @staticmethod
    def _get_font(font: str, points=None):
        font_details = FONTS[font]
        if not points:
            font_size = int(font_details.points / 3 * 4)
        else:
            font_size = int(points / 3 * 4)

        image_font = ImageFont.truetype(font_details.path, font_size)
        return image_font
