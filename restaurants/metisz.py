import json
import os.path
from difflib import get_close_matches
from pathlib import Path

import requests
from easyocr import easyocr
from facebook_page_scraper import Facebook_scraper

from common.constants import DOWNLOAD_DIR, DAY_OF_WEEK, TODAY, DAYS, YEAR_AND_WEEK


class Metisz():
    def __init__(self):
        self.reader = easyocr.Reader(['hu'])
        self.download_dir = f'{DOWNLOAD_DIR}/{YEAR_AND_WEEK}'
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        self.file_path = f'{self.download_dir}/metisz.jpg'
        if not os.path.exists(self.file_path):
            self._download_daily_menu_from_facebook()

    def _download_daily_menu_from_facebook(self):
        posts = Facebook_scraper('metiszkisvendeglo', 1, 'firefox', headless=False)
        post_data = json.loads(posts.scrap_to_json())
        first_post = next(iter((post_data.values())))
        with open(self.file_path, 'wb') as image_file:
            image_file.write(requests.get(first_post['image'][0]).content)


if __name__ == '__main__':
    print(Metisz().file_path)
