import logging
import os

from dotenv import load_dotenv
from slack_sdk import WebClient

from restaurants.bekaplak import Bekaplak
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

panorama = Panorama()
client.files_upload_v2(file_uploads=[
    {"file": panorama.file_path,
     "title": "Panoráma Snack"},
], channel=channel_id, initial_comment='Környékbeli ajánlatok')

# TBD
# kékfény
# metisz
# papírkutya
