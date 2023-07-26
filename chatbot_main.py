import logging
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from slack_sdk import WebClient

from common.constants import DAY_OF_WEEK, DAYS, DOWNLOAD_DIR, YEAR_AND_WEEK
from restaurants.bekaplak import Bekaplak
from restaurants.kekfeny import Kekfeny
from restaurants.metisz import Metisz
from restaurants.panorama import Panorama

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s: %(message)s')

load_dotenv()
client = WebClient(token=os.getenv('SLACK_TOKEN'))
channel_id = os.getenv("CHANNEL_ID")

bekaplak = Bekaplak()
response = client.chat_postMessage(channel=channel_id, text=f'*Bekaplak mai menü* (1990Ft):\n{bekaplak.mai_menu()}')
napi_ajanlatok = f'*Napi ajánlatok*:\n{bekaplak.napi_ajanlat()}'
client.chat_postMessage(channel=channel_id, thread_ts=response['ts'], text=napi_ajanlatok)

weekly_download_dir = f'{DOWNLOAD_DIR}/{YEAR_AND_WEEK}'
Path(weekly_download_dir).mkdir(parents=True, exist_ok=True)

nap = DAYS[DAY_OF_WEEK].lower()
client.files_upload_v2(file_uploads=[
    {"file": Panorama(weekly_download_dir).file_path,
     "title": "Panoráma Snack"},
    {"file": Kekfeny(weekly_download_dir).file_path,
     "title": "Kékfény Étterem"},
    {"file": Metisz(weekly_download_dir).file_path,
     "title": "Metisz Kisvendéglő"},
], channel=channel_id, initial_comment=f'Környékbeli ajánlatok (ma: {datetime.today().strftime("%m.%d.")} {nap})')

# TBD
# papírkutya
