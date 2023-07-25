import os
from datetime import datetime
from pathlib import Path

import requests
from easyocr import easyocr

from common.constants import DOWNLOAD_DIR, USER_AGENT, YEAR_AND_WEEK, WEEK_OF_THE_YEAR


class Panorama:
    def __init__(self):
        self.download_dir = f'{DOWNLOAD_DIR}/{YEAR_AND_WEEK}'
        self.file_path = f'{self.download_dir}/panorama.jpg'
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.file_path):
            self._download_menu_from_website()

    def _download_menu_from_website(self):
        with open(self.file_path, 'wb') as image_file:
            # be aware that pdf exists (instead of ocr?)
            image_file.write(requests.get(f'http://www.panoramasnack.hu/images/menu{WEEK_OF_THE_YEAR}.jpg',
                                          headers={'User-Agent': USER_AGENT}).content)

    def lines(self):
        reader = easyocr.Reader(['hu'])
        result = reader.readtext(self.file_path)
        return [x[1] for x in result[:-1]]


if __name__ == '__main__':
    print(Panorama().lines())
