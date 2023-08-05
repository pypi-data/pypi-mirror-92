## Import and configuration
import json
import re
from googleapiclient.errors import HttpError
import pandas as pd
from configparser import ConfigParser
import sys
import os
import xlrd
from clarku_youtube_crawler.crawlerObject import _CrawlerObject

CONFIG = "config.ini"
config = ConfigParser(allow_no_value=True)
config.read(CONFIG)


class ChannelCrawler(_CrawlerObject):
    def __init__(self):
        super().__init__()
        self.subscriber_cutoff = 0
        self.keyword = None

    def __build__(self):
        self.subscriber_cutoff = int(config.get("main", "default_subscriber_cutoff"))
        super().__build__("channel")

    def setup_channel(self, **kwargs):
        # only use this for filtering, if raw file with no subscribercount, can skip this
        # read a raw json file and save all channels with subscriber greater than subscriber_cutoff
        # Save the channels to channel_list_workfile
        raw_file = kwargs.get("filename", None)  # determine file ext here
        subscriber_cutoff = kwargs.get("subscriber_cutoff", self.subscriber_cutoff)
        self.subscriber_cutoff = subscriber_cutoff
        self.keyword = kwargs.get("keyword", "")

        if raw_file is None:
            print(self.DEFAULT_RAW_FINAL_FILE)
            if os.path.exists(self.DEFAULT_RAW_FINAL_FILE):
                raw_file = self.DEFAULT_RAW_FINAL_FILE
            else:
                raise ValueError("Can't find default raw json. You need to indicate where the raw json file is"
                                 "by using setup_channel(filename = YOUR_PATH")

        channel_list = []
        print(raw_file)
        with open(raw_file, "r") as fp:
            line = fp.readline()
            jobj = json.loads(line)
            while line:
                jobj = json.loads(line)
                if "id" in jobj["channel"]:
                    title = jobj["channel"]["snippet"]["title"] + jobj["channel"]["snippet"]["description"]
                    if "subscriberCount" in jobj["channel"]["statistics"]:
                        channel_list.append({
                            "channelId": jobj["channel"]["id"],
                            "subscriberCount": int(jobj["channel"]["statistics"]["subscriberCount"])
                        })
                line = fp.readline()

        df = pd.DataFrame(channel_list)
        # Find all unique channels
        result = df.groupby(by=df.channelId).subscriberCount.first()
        result = result.sort_values(ascending=False)
        result = pd.DataFrame(result)
        # only keep channels with no less than 10,000 subscribers
        result = result.loc[result.subscriberCount >= self.subscriber_cutoff]
        result.to_csv(self.channel_list_workfile)
        print(f"Successfully filtered channels and saved to {self.channel_list_workfile}")

    # Search all videos in a channel channels.Save videos of a channel in channel_list_dir.
    # Each file contains all videos of the channel
    # JSON returned from https://developers.google.com/youtube/v3/docs/search/list

    def _search_data(self, file_path, channel_id, page_token=None):
        #     print("CURRENT_API: " + DEVELOPER_KEY)
        part = "snippet"
        try:
            if page_token:
                response = self.youtube.search().list(part=part,
                                                      maxResults=50,
                                                      pageToken=page_token,
                                                      type="video",
                                                      channelId=channel_id,
                                                      regionCode="US"
                                                      ).execute()
            else:
                response = self.youtube.search().list(part=part,
                                                      maxResults=50,
                                                      type="video",
                                                      channelId=channel_id,
                                                      regionCode="US"
                                                      ).execute()
            self._write_item(file_path, response["items"], check_duplicate=False)
            return response
        except HttpError as e:
            error = json.loads(e.content)["error"]["errors"][0]["reason"]
            if error == "dailyLimitExceeded" or error == "quotaExceeded":
                self._try_next_id()
                return self._search_data(file_path, channel_id, page_token)  # I assume it's missing one var
        except Exception as e:
            print(e)
            sys.exit(0)
            return "error"

    def _write_item(self, file_path, items, check_duplicate=False):
        if check_duplicate:
            with open(file_path, 'a+') as fp:
                for item in items:
                    item_path = self.channel_data_dir + item["videoId"] + ".json"
                    if not self.isCrawled(item_path):
                        fp.write(json.dumps(item) + "\n")
            return

        with open(file_path, 'a+') as fp:
            for item in items:
                fp.write(json.dumps(item) + "\n")

    def _crawl_data(self, file_name, channel_id):
        response = self._search_data(self.channel_list_dir + file_name, channel_id)
        total_results = response["pageInfo"]["totalResults"]
        print(f"Total videos: {total_results}")
        while response is not None and "nextPageToken" in response:
            response = self._search_data(self.channel_list_dir + file_name, channel_id, response["nextPageToken"])

    def crawl(self, **kwargs):
        filename = kwargs.get("filename", None)
        header = kwargs.get("channel_header", None)
        accepted_ext = [".json", ".csv", ".txt", ".xlsx"]

        if filename:
            file, ext = os.path.splitext(filename)
            if ext not in accepted_ext:
                raise ValueError(f"{ext} is not an accepted file type")
            file = file + ext

        if filename is None:
            print(f"Filename is None. Finding {self.channel_list_workfile}...")
            if os.path.exists(self.channel_list_workfile):
                file = self.channel_list_workfile
                print(f"{self.channel_list_workfile} found successfully!")
                ext = ".json"
                header = "channelId"
            else:
                raise ValueError("Can't find default channel list. You need to indicate where the channel list file is"
                                 "by using crawl(filename=YOUR_PATH)")
        self._crawl_ext(ext, file, header)

    def _crawl_ext(self, ext, filename, header):
        if ext == ".json" or ext == ".csv":
            if not header:
                df = pd.read_csv(filename, encoding="utf-8", header=None)
                channel_list = (channelId.strip() for channelId in df.iloc[:, 0])
            if header:
                try:
                    df = pd.read_csv(filename, encoding="utf-8")
                    df[header]
                    channel_list = (channelId.strip() for channelId in df[header])
                except Exception as e:
                    raise ValueError(f"there is not {header} in this {ext}")
                    print(e)

        if ext == ".xlsx":
            if not header:
                xl = xlrd.open_workbook(filename, encoding_override='utf-8')
                df = pd.read_excel(xl, header=None)
                channel_list = (channelId.strip() for channelId in df.iloc[:, 0])
            if header:
                try:
                    df = pd.read_excel(xl)
                    df[header]
                    channel_list = (channelId.strip() for channelId in df[header])
                except Exception as e:
                    raise ValueError(f"there is not {header} in this {ext}")
                    print(e)

        if ext == ".txt":
            with open(filename, 'r+') as fp:
                channel_list = fp.readlines()
            channel_list = (channelId.strip() for channelId in channel_list)

        for channelId in channel_list:
            print(f"Crawling a video list from {channelId}....")
            if not self.isCrawled(self.channel_list_dir + channelId + ".json"):
                self._crawl_data(channelId + ".json", channelId)

    def _isRelevant(self, search_result, keyword):
        if self.keyword is None:
            return True
        if "videoId" in search_result["id"]:
            if re.search(self.keyword, search_result["snippet"]["title"], re.IGNORECASE):
                return True
            elif "tags" in search_result["snippet"]:
                return keyword.lower() in (tag.lower() for tag in search_result["snippet"])

    def _fetch_metadata(self, keep_relevant=True):
        # Read videos from {channel_list_dir}
        # Save video meta data of all the videos saved in {channel_video_list_workfile}
        video_list = set()
        json_list = (file for file in os.listdir(self.channel_list_dir) if file.endswith(".json"))

        for filename in json_list:
            with open(self.channel_list_dir + filename, 'r') as fp:
                line = fp.readline()
                while line and line != "":
                    search_result = json.loads(line)
                    # Only keeps the videos that contains "keyword" for each video
                    if (keep_relevant and self._isRelevant(search_result, self.keyword)) or not keep_relevant:
                        video_id = ":" + search_result["id"]["videoId"]
                        channel_id = search_result["snippet"]["channelId"]
                        date = search_result["snippet"]["publishedAt"].split("T")[0]
                        video_list.add((video_id, channel_id, date))
                    line = fp.readline()

        df = pd.DataFrame(data=video_list, columns=["videoId", "channelId", "publishedAt"])
        df.to_csv(self.channel_video_list_workfile, index=False)
        print(f"Successfully fetched metadata and saved to {self.channel_video_list_workfile}")

    # comment_page_count: how many pages of comments will be crawled. Each page has 50 comments.
    def crawl_videos_in_list(self, comment_page_count):
        self._fetch_metadata()
        print(f"crawling data from {self.channel_video_list_workfile}....")
        df = pd.read_csv(self.channel_video_list_workfile)
        for index, row in df.iterrows():
            video_id = row["videoId"][1:]  # remove the ":" in the 1st char
            channel_id = row["channelId"]
            filename = video_id + ".json"
            print(filename)
            if not self.isCrawled(self.channel_data_dir + filename):
                video = self.get_video(video_id)
                comments = self.get_comments(video_id, comment_page_count)
                channel = self.get_channel(channel_id)
                caption = self.get_caption(video_id)
                result = {
                    "videoId": video_id,
                    "channelId": channel_id,
                    "video": video,
                    "comments": comments,
                    "channel": channel,
                    "caption": caption,
                }
                with open(self.channel_data_dir + filename, 'w+') as fp:
                    fp.write(json.dumps(result) + "\n")

    def merge_all(self, **kwargs):
        # merge all video jsons into one big json
        video_result_path = kwargs.get("save_to", self.DEFAULT_CHANNEL_FINAL_FILE)
        video_writer = open(video_result_path, "w+")

        json_list = (file for file in os.listdir(self.channel_data_dir) if file.endswith(".json"))
        for filename in json_list:
            with open(self.channel_data_dir + filename, 'r') as fp:
                line = fp.readline()
                while line and line != "":
                    video_writer.write(line)
                    line = fp.readline()

        video_writer.flush()
        video_writer.close()
