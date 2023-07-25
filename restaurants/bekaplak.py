import json
import os.path
import re
from pathlib import Path

import requests
from easyocr import easyocr
from facebook_page_scraper import Facebook_scraper

from common.constants import DOWNLOAD_DIR, DAY_OF_WEEK, TODAY

IGNORED_LINES = [
    '4',  # ez igazából a "A menü zóna adag ételeket tartalmaz" szövegből az "A" betű...
    'A',  # de ha csak önállóan A betűként (sortörés) ismeri fel, azzal se vagyunk beljebb
]


def _merge_lines_split_by_ocr(lines):
    improved_lines = []
    for line in lines:
        if re.search(r'^\d.+', line):  # ha számmal kezdődik, akkor az az ár lesz, de nem túl pontos ez így még
            improved_lines[-1] += f' {line}'
        else:
            improved_lines.append(line)
    return improved_lines


class Bekaplak():
    def __init__(self):
        self.reader = easyocr.Reader(['hu'])
        self.download_dir = f'{DOWNLOAD_DIR}/{TODAY}/bekaplak'
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        if not os.path.exists(f'{self.download_dir}/bekaplak_2.jpg'):
            self._download_daily_menu_from_facebook()

    def _download_daily_menu_from_facebook(self):
        posts = Facebook_scraper('bekaplakonkiszolgaloetterem', 1, 'firefox', headless=False)
        post_data = json.loads(posts.scrap_to_json())
        first_post = next(iter((post_data.values())))
        for i, image_url in enumerate(first_post['image']):
            with open(f'{self.download_dir}/bekaplak_{i}.jpg', 'wb') as image_file:
                image_file.write(requests.get(image_url).content)

    def napi_ajanlat(self):
        result = self.reader.readtext(f'{self.download_dir}/bekaplak_0.jpg')
        lines = [x[1] for x in result[3:]]

        result = self.reader.readtext(f'{self.download_dir}/bekaplak_1.jpg')
        lines += [x[1] for x in result[3:-3]]
        improved_lines = _merge_lines_split_by_ocr(lines)
        return '\n'.join(improved_lines)

    def mai_menu(self):
        result = self.reader.readtext(f'{self.download_dir}/bekaplak_2.jpg')
        lines = [x[1] for x in result[:-1]]
        meals_per_day = {}
        current_day = -1
        for line in lines:
            if line in ['HÉTEÓ', 'HÉTFŐ', 'HÉIFÓ']:
                current_day = 0
                continue
            elif line in ['KEDD']:
                current_day = 1
                continue
            elif line in ['SZERDA']:
                current_day = 2
                continue
            elif line in ['CSÜTÖRTÖK']:
                current_day = 3
                continue
            elif line in ['PÉNTEK', 'PÉNIEK']:
                current_day = 4
                continue
            if line in IGNORED_LINES:
                continue
            if current_day in list(range(5)):
                if current_day in meals_per_day:
                    meals_per_day[current_day].append(line)
                else:
                    meals_per_day[current_day] = [line]
            else:
                continue
        return '\n'.join(meals_per_day[DAY_OF_WEEK])


if __name__ == '__main__':
    print(Bekaplak().napi_ajanlat())
    print('-' * 32 + '\n')
    print(Bekaplak().mai_menu())
