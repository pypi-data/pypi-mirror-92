import requests
import logging
class Sink(object):
    def __init__(self, site, *args, **kwargs):
        self.sink_addr =  os.environ.get("SINK_ADDR", "")
        self.site = site
        self.data_model = kwargs.get('data_model', '')
        self.logger = logging.getLogger(__class__.__name__)
        if self.sink_addr:
             self.sink_session = requests.Session()
    def feed(self, item):
        if not self.sink_addr:
            self.logger.warning(f"no sink_addr, data ignored: {item}")
            return item
        self.logger.debug(f"pipeline {item['source_url']} to sink_addr {self.sink_addr}")
        raw_item = dict(item)
        raw_item['site'] = self.site
        raw_item['url'] = raw_item['source_url']
        res = self.sink_session.post(self.sink_addr, json={
            'model': raw_item.pop('data_model', self.data_model),
            'data': raw_item,
        })
        if res.status_code >= 400 or res.status_code < 200:
            self.logger.error(f"fail to sink {item} for {res.status_code} {res.text}")
