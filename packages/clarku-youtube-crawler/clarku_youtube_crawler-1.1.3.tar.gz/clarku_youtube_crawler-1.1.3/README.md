# clarku-youtube-crawler

Clark University YouTube crawler and JSON decoder for YouTube json. Please read documentation in ``DOCS``

## Installing
To install,

``pip install clarku-youtube-crawler``

The crawler needs multiple other packages to function. 
If missing requirements (I already include all dependencies so it shouldn't happen), download <a href="https://github.com/ClarkUniversity-NiuLab/clarku-youtube-crawler/blob/master/requirements.txt">``requirements.txt`` </a> .
Navigate to the folder where it contains requirements.txt and run 

``pip install -r requirements.txt``

## Example usage
To initialize, 
```
# your_script.py
import clarku_youtube_crawler as cu

test = cu.RawCrawler()
test.__build__()
test.crawl("searchkey",start_date=14, start_month=12, start_year=2020, day_count=2)
test.crawl_videos_in_list(comment_page_count=1)
test.merge_all()

channel = cu.ChannelCrawler()
channel.__build__()
channel.setup_channel(subscriber_cutoff=1000, keyword="")
channel.crawl()
channel.crawl_videos_in_list(comment_page_count=1)
channel.merge_all()

jsonn = cu.JSONDecoder()
jsonn.load_json("YouTube_RAW_20201221/FINAL_raw_merged.json")
```

## Changelog
### ``Version 0.0.1->0.0.3 ``

This is beta without testing since python packaging is a pain. Please don't install these versions.

### ``Version 0.0.5``
Finally figured out testing. It works okay. More documentation to come.

### ``Version 0.0.6``
Stable release only for ``RawCrawler`` feature

### ``Version 1.0.0`` ``Version 1.0.1``
I think this might be our first full stable release.

### ``Version 1.0.1.dev`` ``Pre-release``
Added different file types for ChannelCrawler. Added documentation
