import requests
from bs4 import BeautifulSoup

from common.constants import DAY_OF_WEEK, DAYS, THIS_MONDAY


class Metisz():
    def napi_menu(self):
        etlap = BeautifulSoup(requests.get('https://www.metiszvendeglo.hu/napi-menu/').text, 'html.parser')
        menu_tol_ig = etlap.select('article > div > div.wp-block-cover > div > div > h1')[1].text
        today = THIS_MONDAY.strftime('%Y. %B %-d').casefold()
        assert menu_tol_ig.casefold().startswith(today)
        mai_selector = f'#main .wp-block-group:nth-child({DAY_OF_WEEK + 3}) h3'
        a_menu = '\n'.join([f'*A menü* ({DAYS[DAY_OF_WEEK].lower()})'] + [e.text for e in etlap.select(mai_selector)])
        b_menu_selector = f'#main .wp-block-group:nth-child(8) h3'
        b_menu = '\n'.join(['*B menü*'] + [e.text for e in etlap.select(b_menu_selector)])
        return f'{a_menu}\n{b_menu}'

    def etlap(self):
        etlap = BeautifulSoup(requests.get('https://www.metiszvendeglo.hu/etlap/').text, 'html.parser')
        results = []
        for i in range(4, 4 + len(etlap.select('#main .wp-block-heading')), 2):
            results.append('*' + etlap.select(f'#main h2.wp-block-heading:nth-child({i})')[0].text + '*')
            results += ['  ' + i.text for i in etlap.select(f'#main figure.wp-block-table:nth-child({i + 1}) tr')]
        return '\n'.join(results)


if __name__ == '__main__':
    import locale

    locale.setlocale(locale.LC_TIME, "hu_HU")
    metisz = Metisz()
    print(metisz.napi_menu())
    print(metisz.etlap())
