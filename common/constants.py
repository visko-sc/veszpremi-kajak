from datetime import datetime, timedelta

from os.path import dirname

PROJECT_ROOT = dirname(dirname(__file__))
DOWNLOAD_DIR = f'{PROJECT_ROOT}/download'

TODAY_DT = datetime.today()
TODAY = TODAY_DT.strftime('%Y-%m-%d')
WEEK_OF_THE_YEAR = TODAY_DT.isocalendar()[1]
YEAR_AND_WEEK = TODAY_DT.strftime('%Yw%W')
DAY_OF_WEEK = TODAY_DT.weekday()

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/114.0.0.0 Safari/537.36'
}  # else we get 403 :(

DAYS = ['HÉTFŐ', 'KEDD', 'SZERDA', 'CSÜTÖRTÖK', 'PÉNTEK']
THIS_MONDAY = TODAY_DT - timedelta(days=TODAY_DT.weekday())
THIS_MONDAY_0_AM = THIS_MONDAY.replace(hour=0, minute=0, second=0, microsecond=0)
LAST_UPDATED_PATTERN = "%a, %d %b %Y %H:%M:%S %Z"
