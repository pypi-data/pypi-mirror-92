import sys
from googleapiclient.discovery import build
import json
from googleapiclient.errors import HttpError
from configparser import ConfigParser
import os
from httplib2 import ServerNotFoundError
from youtube_transcript_api import YouTubeTranscriptApi

CONFIG = "config.ini"
config = ConfigParser(allow_no_value=True)
config.read(CONFIG)
TIME_DELTA = int(config.get("main", "default_time_crawler"))
DEFAULT_RAW_FINAL_FILE = "FINAL_raw_merged.json"  # within {RAW_PARENT_PATH}
DEFAULT_CHANNEL_FINAL_FILE = "FINAL_channel_merged.json"  # within {CHANNEL_PARENT_PATH}

# TODO: Work on setup_channel for different extensions

class _CrawlerObject():
    def __init__(self):
        # more permanent
        self.DEVELOPER_KEY = None
        self.YOUTUBE_API_SERVICE_NAME = None
        self.YOUTUBE_API_VERSION = None
        self.KEYS_PATH = None
        self.TIME_DELTA = None
        self.DEFAULT_RAW_FINAL_FILE = None
        self.DEFAULT_CHANNEL_FINAL_FILE = None
        self.codes = []

        # more changing
        self.youtube = None
        self.search_key = None
        self.code_index = -1

        # depends more on user's config
        self.RAW_PARENT_PATH = None
        self.video_list_workfile = None
        self.video_list_dir = None
        self.video_data_dir = None

        self.CHANNEL_PARENT_PATH = None
        self.channel_data_dir = None
        self.channel_list_dir = None
        self.channel_list_workfile = None
        self.channel_video_list_workfile = None

    def __build__(self, objectType):
        self._fetch_vars()
        raw_dest_list = [self.RAW_PARENT_PATH, self.video_list_dir, self.video_data_dir]
        channel_dest_list = [self.CHANNEL_PARENT_PATH, self.channel_list_dir, self.channel_data_dir]
        if objectType == "raw":
            destination_list = raw_dest_list
        if objectType == "channel":
            destination_list = channel_dest_list
        for dest in destination_list:
            try:
                os.mkdir(dest)
            except OSError:
                print("Directory already exists %s" % dest)
            else:
                print("Successfully created the directory %s " % dest)
        self.DEFAULT_RAW_FINAL_FILE = f"{self.RAW_PARENT_PATH}{DEFAULT_RAW_FINAL_FILE}"
        self.DEFAULT_CHANNEL_FINAL_FILE = f"{self.CHANNEL_PARENT_PATH}{DEFAULT_CHANNEL_FINAL_FILE}"

        # api
        try:
            self._try_next_id()
            self.youtube = build(
                self.YOUTUBE_API_SERVICE_NAME,
                self.YOUTUBE_API_VERSION,
                developerKey=self.DEVELOPER_KEY,
                cache_discovery=False)
            print("BUILD SUCCESS")
        except ServerNotFoundError:
            print("BUILD FAILED - NO INTERNET CONNECTION")
            sys.exit(0)

    def _fetch_vars(self):
        config.read(CONFIG)
        self.TIME_DELTA = int(config.get("main", "default_time_crawler"))
        self.YOUTUBE_API_SERVICE_NAME = config.get("api", "youtube_api_service_name")
        self.YOUTUBE_API_VERSION = config.get("api", "youtube_api_version")
        self.KEYS_PATH = config.get("api", "keys_path")
        with open(self.KEYS_PATH, 'r+') as fp:
            self.codes = fp.readlines()

        # channel
        self.CHANNEL_PARENT_PATH = config.get("channelfilepath", "channel_parent_path")
        self.channel_video_list_workfile = \
            self.CHANNEL_PARENT_PATH + config.get("channelfilepath", "channel_video_list_workfile")
        self.channel_list_workfile = \
            self.CHANNEL_PARENT_PATH + config.get("channelfilepath", "channel_list_workfile")
        self.channel_list_dir = \
            self.CHANNEL_PARENT_PATH + config.get("channelfilepath", "channel_list_dir")
        self.channel_data_dir = \
            self.CHANNEL_PARENT_PATH + config.get("channelfilepath", "channel_data_dir")

        # raw
        self.RAW_PARENT_PATH = config.get("rawfilepath", "raw_parent_path")
        self.video_list_workfile = \
            self.RAW_PARENT_PATH + config.get("rawfilepath", "video_list_workfile")
        self.video_list_dir = \
            self.RAW_PARENT_PATH + config.get("rawfilepath", "video_list_dir")
        self.video_data_dir = \
            self.RAW_PARENT_PATH + config.get("rawfilepath", "video_data_dir")

    # Try update the API
    def _try_next_id(self):
        if self.code_index + 1 < len(self.codes):
            self.code_index += 1
            self.DEVELOPER_KEY = self.codes[self.code_index].strip()  # Update a new key
            self.youtube = build(
                self.YOUTUBE_API_SERVICE_NAME,
                self.YOUTUBE_API_VERSION,
                developerKey=self.DEVELOPER_KEY,
                cache_discovery=False)
            print(f"Update Developer Key:{self.DEVELOPER_KEY}")
        else:
            print("running out keys")
            sys.exit(0)
        self.DEVELOPER_KEY = self.codes[self.code_index].strip()  # Use your own Keys.

    # The crawler will iterate each video id in video_list_workfile.csv and get video, channel,
    # comment, and caption data. Each video is saved in an individual json in video_data.
    def get_video(self, video_id):
        part = "id,snippet,statistics,contentDetails"
        try:
            response = self.youtube.videos().list(part=part,
                                                  maxResults=1,
                                                  id=video_id).execute()
            if len(response["items"]) == 0:
                return "error"
            return response["items"][0]
        except HttpError as e:
            error = json.loads(e.content)["error"]["errors"][0]["reason"]
            if error == "dailyLimitExceeded" or error == "quotaExceeded":
                self._try_next_id()
                return self.get_video(video_id)
        except Exception as e:
            return "error"

    # Save video comments of all the videos saved in {channel_list_dir}
    # JSON returned from https://developers.google.com/youtube/v3/docs/comments
    def get_comments(self, video_id, comment_page_count):
        part = "snippet"
        try:
            response = self.youtube.commentThreads().list(part=part,
                                                          maxResults=50,
                                                          videoId=video_id).execute()
            comments = response["items"]
            counter = 0  # save the first page_count pages
            while "nextPageToken" in response:
                page_token = response["nextPageToken"]
                response = self.youtube.commentThreads().list(part=part,
                                                              maxResults=50,
                                                              videoId=video_id,
                                                              pageToken=page_token).execute()
                comments += response["items"]
                if counter == comment_page_count:
                    return comments
                counter += 1
            return comments
        except HttpError as e:
            error = json.loads(e.content)["error"]["errors"][0]["reason"]
            if error == "dailyLimitExceeded" or error == "quotaExceeded":
                self._try_next_id()
                return self.get_comments(video_id, comment_page_count)
        except Exception as e:
            return "error"

    # Save channel info of all the videos saved in {video_list_dir}
    def get_channel(self, channel_id):
        try:
            part = "id,snippet,statistics,contentDetails,topicDetails,brandingSettings,contentOwnerDetails," \
                   "localizations "
            response = self.youtube.channels().list(part=part, maxResults=1, id=channel_id).execute()
            return response["items"][0]
        except HttpError as e:
            error = json.loads(e.content)["error"]["errors"][0]["reason"]
            if error == "dailyLimitExceeded" or error == "quotaExceeded":
                self._try_next_id()
                return self.get_channel(channel_id)
        except Exception as e:
            return "error"

    # Save closed captions info of all the videos saved in {video_list_path}
    def get_caption(self, video_id):
        caption = []
        try:
            caption = YouTubeTranscriptApi.get_transcript(video_id)
            return caption
        except Exception as e:
            # print(e)
            return "error"

    def toDayFormat(self, date):
        return f"{date.month}-{date.day}-{date.year}"

    def isCrawled(self, file_name):
        return os.path.exists(file_name)

    def _write_item(self, file_path, items):
        with open(file_path, 'a+') as fp:
            for item in items:
                fp.write(json.dumps(item) + "\n")
