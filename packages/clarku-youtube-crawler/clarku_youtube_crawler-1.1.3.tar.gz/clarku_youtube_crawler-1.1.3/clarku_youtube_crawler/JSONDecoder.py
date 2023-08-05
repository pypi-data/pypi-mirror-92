import json
import isodate
import pandas as pd
import os
import pkgutil

save_directory = "YouTube_CSV/"

numerr_flag = -1
strerr_flag = "unknown"

cate_data = pkgutil.get_data(__name__, "US_CATE.json")
US_CATE = json.loads(cate_data.decode("utf-8"))

class JSONDecoder():
    def __init__(self):
        try:
            os.mkdir(save_directory)
        except OSError:
            print("Directory already exists %s" % save_directory)
        else:
            print("Successfully created the directory %s " % save_directory)

    def filter_video(self, video):
        #     print(json.dumps(video["video"]["snippet"]))
        #     time = dateutil.parser.parse(video["video"]["snippet"]["publishedAt"])
        #     if time < datetime.datetime(year=2020, month=3, day=11, hour=0, minute=0, second=0, tzinfo=pytz.UTC):
        #         return False
        #     if time > datetime.datetime(year=2020, month=5, day=16, hour=0, minute=0, second=0, tzinfo=pytz.UTC):
        #         return False
        if video["channel"] == "error" or video["channel"] == ["error"]:
            return False
        return True

    def get_duration(self, duration):
        dur = isodate.parse_duration(duration)
        return dur.total_seconds()

    def get_video_category(self, channel, categoryId):
        categories = []
        if "videoCategories" not in channel:
            categories = US_CATE
        else:
            categories = channel["videoCategories"]["items"]
        for cate in categories:
            if cate["id"] == categoryId:
                return cate["snippet"]["title"]
        for cate in US_CATE:
            if cate["id"] == categoryId:
                return cate["snippet"]["title"]

    def get_caption_list(self, captions):
        caption = []
        if captions == "error" or captions == ["error"]:
            return caption
        for cap in captions:
            caption.append(cap["text"])
        return json.dumps(caption)

    def get_video_obj(self, data):
        if data["video"] == "error":
            return None
        if "localized" not in data["video"]["snippet"] or "channelId" not in data["video"]["snippet"]:
            return None
        return {
            # video_info
            "embedUrl": "https://www.youtube.com/embed/{0}".format(data["video"]["id"]),
            "videoId": ":" + data["video"]["id"],
            "channelId": data["video"]["snippet"]["channelId"],
            "title": data["video"]["snippet"]["localized"]["title"],
            "tags": json.dumps(data["video"]["snippet"]["tags"]) if "tags" in data["video"]["snippet"] else "[]",
            "duration": self.get_duration(data["video"]["contentDetails"]["duration"]),
            "publishedAt": data["video"]["snippet"]["publishedAt"],
            "categoryId": data["video"]["snippet"]["categoryId"],
            "categories": self.get_video_category(data["channel"], data["video"]["snippet"]["categoryId"]),
            "description": data["video"]["snippet"]["localized"]["description"],
            "tags": data["video"]["snippet"]["tags"] if "tags" in data["video"]["snippet"] else [],
            "commentCount": int(data["video"]["statistics"]["commentCount"]) if "commentCount" in data["video"][
                "statistics"] else numerr_flag,
            "viewCount": int(data["video"]["statistics"]["viewCount"]) if "viewCount" in data["video"][
                "statistics"] else numerr_flag,
            "likeCount": int(data["video"]["statistics"]["likeCount"]) if "likeCount" in data["video"][
                "statistics"] else numerr_flag,
            "dislikeCount": int(data["video"]["statistics"]["dislikeCount"]) if "dislikeCount" in data["video"][
                "statistics"] else numerr_flag,
            "videoUrl": "https://www.youtube.com/watch?v={0}".format(data["video"]["id"]),
            #             "caption": get_caption_list(data["caption"]),
            "country": data["channel"]["snippet"]["country"] if "country" in data["channel"]["snippet"] else strerr_flag,
            "defaultAudioLanguage": data["video"]["snippet"]["defaultAudioLanguage"] if "defaultAudioLanguage" in data["video"]["snippet"] else strerr_flag,
        }

    def get_category(self, channel):
        result = []
        if "topicDetails" in channel and "topicCategories" in channel["topicDetails"]:
            cate_list = channel["topicDetails"]["topicCategories"]
            for cate in cate_list:
                result.append(cate.split('/')[-1])
        return result

    def get_channel_obj(self, data):
        return {
            "channelId": data["channel"]["id"],
            "title": data["channel"]["snippet"]["localized"]["title"],
            "description": data["channel"]["snippet"]["localized"]["description"],
            "subscriberCount": int(data["channel"]["statistics"]["subscriberCount"]) if "subscriberCount" in
                                                                                        data["channel"][
                                                                                            "statistics"] else strerr_flag,
            "publishedAt": data["channel"]["snippet"]["publishedAt"] if "publishedAt" in data["channel"][
                "snippet"] else strerr_flag,
            "country": data["channel"]["snippet"]["country"] if "country" in data["channel"][
                "snippet"] else strerr_flag,
            "videoCount": int(data["channel"]["statistics"]["videoCount"]),
            "KEYWORDVideoCount": 1,
            "viewCount": int(data["channel"]["statistics"]["viewCount"]),
            "topicCategories": self.get_category(data["channel"]),
        }

    def get_comment_obj(self, data):
        if data["comments"] and data["comments"] != "error":
            comments = []
            for c in data["comments"]:
                if "channel" not in data["video"]:
                    continue
                comments.append({
                    "embedUrl": "https://www.youtube.com/embed/{0}".format(data["video"]["id"]),
                    "commentId": c["snippet"]["topLevelComment"]["id"] if "topLevelComment" in c[
                        "snippet"] else strerr_flag,
                    "channelId": data["channel"]["id"],
                    "videoId": ":" + data["video"]["id"],
                    "authorDisplayName": c["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                    "authorChannelId": c["snippet"]["topLevelComment"]["snippet"]["authorChannelId"][
                        "value"] if "authorChannelId" in c["snippet"]["topLevelComment"][
                        "snippet"] else numerr_flag,
                    "likeCount": c["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                    "publishedAt": c["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                    "totalReplyCount": c["snippet"]["totalReplyCount"],
                    "textDisplay": c["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                })
            return comments
        else:
            return None
        
    def _save_to_csv(self, dlist, name):
        df = pd.DataFrame(data=dlist)
        df.to_csv(save_directory + name, index=False)

    def load_json(self, data_file):

        video_list = []
        channel_dict = {}
        comment_list = []

        with open(data_file, "r") as fp:
            line = fp.readline()

            while line:
                dataobj = json.loads(line)
                if self.filter_video(dataobj):
                    # get video information
                    video = self.get_video_obj(dataobj)
                    if video:
                        video_list.append(video)

                    # get channel information
                    channel = self.get_channel_obj(dataobj)
                    if channel:
                        channelId = channel["channelId"]
                        if channelId not in channel_dict:
                            channel_dict[channelId] = channel
                        else:
                            channel_dict[channelId]["KEYWORDVideoCount"] += 1

                    # get comment information
                    comments = self.get_comment_obj(dataobj)
                    if comments:
                        comment_list.extend(comments)
                line = fp.readline()

        save_name, _ = os.path.splitext(os.path.basename(data_file))
        self._save_to_csv(video_list, f"video_{save_name}.csv")
        self._save_to_csv(channel_dict.values(), f"channel_{save_name}.csv")
        self._save_to_csv(comment_list, f"comment_{save_name}.csv")
        print(f"Saved files to {save_directory}")