from datetime import datetime
from os.path import dirname

PROJECT_ROOT = dirname(dirname(__file__))
DOWNLOAD_DIR = f'{PROJECT_ROOT}/download'
TODAY = datetime.today().strftime('%Y-%m-%d')
WEEK_OF_THE_YEAR = datetime.today().isocalendar()[1]
YEAR_AND_WEEK = datetime.today().strftime('%Yw%W')
DAY_OF_WEEK = datetime.today().weekday()

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)' \
             ' Chrome/114.0.0.0 Safari/537.36'  # else we get 403 :(

DAYS = ['HÉTFŐ', 'KEDD', 'SZERDA', 'CSÜTÖRTÖK', 'PÉNTEK']
