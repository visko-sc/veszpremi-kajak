import locale
import logging
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from slack_sdk import WebClient

from common.constants import DAY_OF_WEEK, DAYS, DOWNLOAD_DIR, YEAR_AND_WEEK
from restaurants.allegro import Allegro
from restaurants.bekaplak import Bekaplak
from restaurants.kekfeny import Kekfeny
from restaurants.metisz import Metisz
from restaurants.panorama import Panorama

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s: %(message)s')

load_dotenv()
client = WebClient(token=os.getenv('SLACK_TOKEN'))
channel_id = os.getenv("CHANNEL_ID")
locale.setlocale(locale.LC_TIME, "hu_HU")

bekaplak = Bekaplak()
response = client.chat_postMessage(channel=channel_id, text=f'*Bekaplak mai menü* (1990Ft):\n{bekaplak.mai_menu()}')
napi_ajanlatok = f'*Napi ajánlatok*:\n{bekaplak.napi_ajanlat()}'
client.chat_postMessage(channel=channel_id, thread_ts=response['ts'], text=napi_ajanlatok)

allegro = Allegro()
response = client.chat_postMessage(channel=channel_id, text=f'*Allegro napi menü* (1890Ft):\n{allegro.napi_menu()}')
client.chat_postMessage(channel=channel_id, thread_ts=response['ts'], text=allegro.napi_ajanlat())

metisz = Metisz()
response = client.chat_postMessage(channel=channel_id, text=f'*Metisz napi menü* (2300Ft):\n{metisz.napi_menu()}')
client.chat_postMessage(channel=channel_id, thread_ts=response['ts'], text=metisz.etlap())

weekly_download_dir = f'{DOWNLOAD_DIR}/{YEAR_AND_WEEK}'
Path(weekly_download_dir).mkdir(parents=True, exist_ok=True)

nap = DAYS[DAY_OF_WEEK].lower()
try:
    client.files_upload_v2(file_uploads=[
        {"file": Panorama(weekly_download_dir).file_path,
         "title": "Panoráma Snack"},
        {"file": Kekfeny(weekly_download_dir).file_path,
         "title": "Kékfény Étterem"},
    ], channel=channel_id, initial_comment=f'Környékbeli ajánlatok (ma: {datetime.today().strftime("%m.%d.")} {nap})')
except:  # noqa
    client.chat_postMessage(channel=channel_id, text=f'Panoráma vagy Kékfény még nem töltötte fel az ehetit')

# TBD
# papírkutya
