from configparser import ConfigParser
from datetime import date
import os

# You can configure here or in the generated config.ini file
# If you configure directly in this code, make sure to delete existing config.ini to reflect the changes
__all__ = ['rawCrawler', 'channelCrawler', 'jSONDecoder']
__version__ = '1.1.3'

CONFIG = "config.ini"
DATE = str(date.today()).replace("-", "")  # today in yyyymmdd
RAW_PARENT_PATH = f"YouTube_RAW_{DATE}/"
CHANNEL_PARENT_PATH = f"YouTube_CHANNEL_{DATE}/"

global OVERRIDE_CONFIG
OVERRIDE_CONFIG = False


def config_override(bool):
    global OVERRIDE_CONFIG
    OVERRIDE_CONFIG = bool
    if OVERRIDE_CONFIG or (not OVERRIDE_CONFIG and os.path.exists(CONFIG)):
        generate_config()


def generate_config():
    if os.path.exists(CONFIG):
        os.remove(CONFIG)
    main = {
        "default_time_crawler": "7",  # if no start date for crawl, go back this many days from today
        "default_subscriber_cutoff": "10000",
        "default_comment_page_count": "4",
    }

    rawfilepath = {
        "RAW_PARENT_PATH": f"YouTube_RAW_{DATE}/",
        "VIDEO_LIST_WORKFILE": f"/video_list.csv",
        "VIDEO_LIST_DIR": f"/video_list/",
        "VIDEO_DATA_DIR": f"/video_data/"
    }

    channelfilepath = {
        "CHANNEL_PARENT_PATH": f"YouTube_CHANNEL_{DATE}/",
        "CHANNEL_LIST_WORKFILE": "/channel_list.csv",
        "CHANNEL_VIDEO_LIST_WORKFILE": f"/channel_video_list.csv",
        "CHANNEL_LIST_DIR": f"/channel_list/",
        "CHANNEL_DATA_DIR": f"/channel_data/"
    }

    api = {
        "KEYS_PATH": "DEVELOPER_KEY.txt",
        "YOUTUBE_API_SERVICE_NAME": "youtube",
        "YOUTUBE_API_VERSION": "v3",
        "YOUTUBE_URL": "https://www.googleapis.com/youtube/v3/"
    }

    config = ConfigParser(allow_no_value=True)
    config.read(CONFIG)

    config.add_section('main')
    config.set('main', '; default_time_crawler: if no start date for crawl, go back this many days from today')
    for k, v in main.items():
        config.set("main", k, v)

    config.add_section('rawfilepath')
    config.set('rawfilepath', '; all sub directories in this section will be under RAW_PARENT_PATH')
    for k, v in rawfilepath.items():
        config.set("rawfilepath", k, v)

    config.add_section('channelfilepath')
    config.set('channelfilepath', '; all sub directories in this section will be under CHANNEL_PARENT_PATH')
    for k, v in channelfilepath.items():
        config.set("channelfilepath", k, v)

    config.add_section('api')
    for k, v in api.items():
        config.set("api", k, v)

    with open(CONFIG, 'w') as f:
        config.write(f)


if not os.path.exists(CONFIG):
    generate_config()

from clarku_youtube_crawler.channelCrawler import ChannelCrawler
from clarku_youtube_crawler.rawCrawler import RawCrawler
from clarku_youtube_crawler.jSONDecoder import JSONDecoder
