#!/usr/bin/python3
# coding: utf-8

import time
from flipdotapi.text_builder import TextBuilder
from flipdotapi.simulator import flipdotSim
import requests
import logging
import json


class remote_sign:

    LETTERS_PER_LINE = 12
    LINE1_START = 0
    LINE2_START = 8
    LOG_LEVEL = logging.DEBUG

    def __init__(self, url, cols, rows, simulator=False):
        # Create a serial port (update with port name on your system)
        logging.basicConfig(level=self.LOG_LEVEL)
        self.logger = logging.getLogger(__name__)
        self.url = url
        self.columns = cols
        self.rows = rows
        self.text_builder = TextBuilder(cols, rows)

        if simulator:
            self.simulator = flipdotSim(self.columns, self.rows)

    def clear(self):
        self.logger.debug("erasing")
        empty = self.sign.create_image()
        self.render_image(empty)

    def render_image(self, image_data):
        image_array = image_data.tolist()
        headers = {'Content-type': 'application/json'}
        r = requests.post(self.url, data=json.dumps(image_array), headers=headers)



    def write_text(self, text, alignment="centre", font_name="nintendo-entertainment-system-regular", fit=False):
        self.logger.debug("sending text to sign: " + text)
        images = self.text_builder.text_image(
            text, font_name=font_name, alignment=alignment, fit=fit)

        for _, image in enumerate(images):
            self.render_image(image)
