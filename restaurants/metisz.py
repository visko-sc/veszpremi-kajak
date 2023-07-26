import json
import os.path

import requests
from facebook_page_scraper import Facebook_scraper


class Metisz():
    def __init__(self, download_dir: str):
        self.file_path = f'{download_dir}/metisz.jpg'
        if not os.path.exists(self.file_path):
            self._download_daily_menu_from_facebook()

    def _download_daily_menu_from_facebook(self):
        posts = Facebook_scraper('metiszkisvendeglo', 1, 'firefox', headless=False)
        post_data = json.loads(posts.scrap_to_json())
        first_post = next(iter((post_data.values())))
        with open(self.file_path, 'wb') as image_file:
            image_file.write(requests.get(first_post['image'][0]).content)


if __name__ == '__main__':
    from pathlib import Path
    from common.constants import DOWNLOAD_DIR, YEAR_AND_WEEK

    weekly_download_dir = f'{DOWNLOAD_DIR}/{YEAR_AND_WEEK}'
    Path(weekly_download_dir).mkdir(parents=True, exist_ok=True)
    print(Metisz(weekly_download_dir).file_path)
