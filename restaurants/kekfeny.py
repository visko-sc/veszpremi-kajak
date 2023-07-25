import os
from pathlib import Path

import requests
from easyocr import easyocr

from common.constants import DOWNLOAD_DIR, YEAR_AND_WEEK, USER_AGENT


class Kekfeny:
    def __init__(self):
        self.download_dir = f'{DOWNLOAD_DIR}/{YEAR_AND_WEEK}'
        self.file_path = f'{self.download_dir}/kekfeny.png'
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.file_path):
            self._download_menu_from_website()

    def _download_menu_from_website(self):
        with open(self.file_path, 'wb') as image_file:
            image_file.write(requests.get('https://www.etel-hazhozszallitas.hu/images/etlap/etlap.png',
                                          headers={'User-Agent': USER_AGENT}).content)

    def lines(self):
        reader = easyocr.Reader(['hu'])
        result = reader.readtext(self.file_path)
        return [x[1] for x in result[:-1]]


if __name__ == '__main__':
    print(Kekfeny().file_path)
