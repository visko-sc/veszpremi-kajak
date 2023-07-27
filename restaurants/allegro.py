import locale
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class Allegro():
    def __init__(self):
        self.etlap = BeautifulSoup(requests.get('https://allegrocafe.hu/').text, 'html.parser')
        today = datetime.today().strftime('%Y. %B %d').casefold()
        assert self.etlap.select('.daily-menu h3')[0].text.strip().casefold().startswith(today)

    def napi_menu(self):
        lines = self.etlap.select('.categories .category:nth-child(1) .items .row')
        return '\n'.join(line.text.strip() for line in lines)

    def napi_ajanlat(self):
        blocks = []
        categories = self.etlap.select('.categories .category')
        for i in range(1, len(categories)):
            blocks.append(f'*{categories[i].select(".name h4")[0].text.capitalize()}*')
            blocks.append('  ' + '\n  '.join(i.text for i in categories[i].select(".items .row")))
        return '\n'.join(blocks)


if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, "hu_HU")
    print('Napi menü:\n' + Allegro().napi_menu())
    print('-' * 32 + '\n')
    print(Allegro().napi_ajanlat())
