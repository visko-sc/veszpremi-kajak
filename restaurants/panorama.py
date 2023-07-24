import os
from datetime import datetime
from os.path import dirname
from pathlib import Path

import requests
from easyocr import easyocr

from common.constants import DOWNLOAD_DIR

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)' \
             ' Chrome/114.0.0.0 Safari/537.36'  # else we get 403 :(


class Panorama:
    def __init__(self):
        self.reader = easyocr.Reader(['hu'])
        today = datetime.today().strftime('%Y-%m-%d')
        self.download_dir = f'{DOWNLOAD_DIR}/{today}'
        self.file_path = f'{self.download_dir}/panorama.jpg'
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.file_path):
            self._download_daily_menu_from_facebook()

    def _download_daily_menu_from_facebook(self):
        week_of_the_year = datetime.today().isocalendar()[1]
        with open(self.file_path, 'wb') as image_file:
            # be aware that pdf exists (instead of ocr?)
            image_file.write(requests.get(f'http://www.panoramasnack.hu/images/menu{week_of_the_year}.jpg',
                                          headers={'User-Agent': USER_AGENT}).content)

    def lines(self):
        result = self.reader.readtext(self.file_path)
        return [x[1] for x in result[:-1]]


if __name__ == '__main__':
    print(Panorama().lines())
