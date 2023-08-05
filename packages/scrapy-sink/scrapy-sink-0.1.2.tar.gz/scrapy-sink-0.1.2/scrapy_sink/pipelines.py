import requests
import logging
import os

logger = logging.getLogger(__name__)


class SinkPipeline:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if self.sink_addr:
            self.sink_session = requests.Session()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sink_addr=crawler.settings.get('SINK_ADDR', os.environ.get("SINK_ADDR")),
        )

    def process_item(self, item, spider):
        if self.sink_addr:
            logger.debug(f"pipeline {item['source_url']} to sink_addr {self.sink_addr}")
            raw_item = dict(item)
            raw_item['site'] = spider.name
            raw_item['url'] = raw_item['source_url']
            self.sink_session.post(self.sink_addr, json={
                'model': raw_item.pop('data_model', getattr(spider, 'data_model', '')),
                'data': raw_item,
            })
        return item
