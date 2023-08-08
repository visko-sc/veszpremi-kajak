import locale
import os
from datetime import datetime

import requests
from easyocr import easyocr

from common.constants import USER_AGENT, LAST_UPDATED_PATTERN, THIS_MONDAY_0_AM


class Kekfeny:
    def __init__(self, download_dir: str):
        self.file_path = f'{download_dir}/kekfeny.png'
        if not os.path.exists(self.file_path):
            self._download_menu_from_website()

    def _download_menu_from_website(self):
        response = requests.get('https://www.etel-hazhozszallitas.hu/images/etlap/etlap.png', headers=USER_AGENT)
        locale_to_restore = locale.getlocale()
        locale.setlocale(locale.LC_TIME, "en_US")
        last_modified_ts = datetime.strptime(response.headers['last-modified'], LAST_UPDATED_PATTERN).timestamp()
        locale.setlocale(locale.LC_TIME, locale_to_restore[0])
        assert THIS_MONDAY_0_AM.timestamp() < last_modified_ts
        with open(self.file_path, 'wb') as image_file:
            image_file.write(response.content)

    def lines(self):
        reader = easyocr.Reader(['hu'])
        result = reader.readtext(self.file_path)
        return [x[1] for x in result[:-1]]


if __name__ == '__main__':
    from pathlib import Path
    from common.constants import DOWNLOAD_DIR, YEAR_AND_WEEK

    weekly_download_dir = f'{DOWNLOAD_DIR}/{YEAR_AND_WEEK}'
    Path(weekly_download_dir).mkdir(parents=True, exist_ok=True)
    print(Kekfeny(weekly_download_dir).file_path)
