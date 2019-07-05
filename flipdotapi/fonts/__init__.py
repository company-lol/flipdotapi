import os
from collections import namedtuple
import fnmatch
from fontTools import ttLib
from slugify import slugify
import logging

class fonts:
    
    FONT_DIRECTORY = os.path.join(os.path.dirname(__file__), './')
    LOG_LEVEL = logging.INFO

    def __init__(self):
        logging.basicConfig(level=self.LOG_LEVEL)
        self.logger = logging.getLogger(__name__)

    def shortName(self,  font ):
        FONT_SPECIFIER_NAME_ID = 4
        FONT_SPECIFIER_FAMILY_ID = 1
        name = ""
        family = ""
        for record in font['name'].names:
            if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
                name = record.string.decode('utf-8')
            elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family:
                family = record.string.decode('utf-8')
            if name and family:
                break
        return name, family

    def get_font_files(self, dir_name=None):

        font_files = []
        font_pattern = '*.ttf'

        if not dir_name:
            dir_name = self.FONT_DIRECTORY
        
        for root, dirs, files in os.walk(dir_name):
            for filename in fnmatch.filter(files, font_pattern):               
                tt = ttLib.TTFont(os.path.join(root, filename))
                name = slugify(self.shortName(tt)[0])
                font_dir = root.replace(dir_name,"")
                font_obj = {"name":name, "filename":filename, "path":font_dir}
                font_files.append(font_obj)

        return font_files


    def _font_path(self, path):
        return os.path.join(self.FONT_DIRECTORY, path)

    def get_fonts(self):
        TrueTypeFont = namedtuple('TrueTypeFont', ['path', 'points'])
        fonts = {}
        font_files = self.get_font_files()
        for f in font_files:
            name = f['name']
            fonts[name] =  TrueTypeFont(
                self._font_path(f['path'] + "/" + f['filename']), 8)

        return fonts #self.FONTS
    




