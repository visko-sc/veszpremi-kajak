import os

import requests
from easyocr import easyocr

from common.constants import USER_AGENT, WEEK_OF_THE_YEAR


class Panorama:
    def __init__(self, download_dir: str):
        self.file_path = f'{download_dir}/panorama.jpg'
        if not os.path.exists(self.file_path):
            self._download_menu_from_website()

    def _download_menu_from_website(self):
        with open(self.file_path, 'wb') as image_file:
            # be aware that pdf exists (instead of ocr?)
            image_file.write(requests.get(f'http://www.panoramasnack.hu/images/menu{WEEK_OF_THE_YEAR}.jpg',
                                          headers=USER_AGENT).content)

    def lines(self):
        reader = easyocr.Reader(['hu'])
        result = reader.readtext(self.file_path)
        return [x[1] for x in result[:-1]]


if __name__ == '__main__':
    from pathlib import Path
    from common.constants import DOWNLOAD_DIR, YEAR_AND_WEEK

    weekly_download_dir = f'{DOWNLOAD_DIR}/{YEAR_AND_WEEK}'
    Path(weekly_download_dir).mkdir(parents=True, exist_ok=True)

    print(Panorama(weekly_download_dir).lines())
