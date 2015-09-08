from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest

from xueqiu.items import Weibo

import json
import time


class statement(Spider):
    name = "statement"
    allowed_domains = ["xueqiu.com"]
    weibo = Weibo()
    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://xueqiu.com
        @scrapes name
        """
        
        sel = Selector(response)
        self.user_id = 5869947685
        # get cubes
        yield FormRequest('http://xueqiu.com/statuses/search.json',
         callback=self.weibos,
         method='get',
         formdata={
         'symbol': 'SH600255',
         'page': 1,
         'ex': 1,
         'uid': self.user_id,
         'sort': 'time',
         'comment': 0,
         '_': str(int(time.time()))
         })

    def weibos(self, response):
        self.weibo['user_id'] = self.user_id
        self.weibo['weibosList'] = json.loads(response.body)['list']
        yield self.weibo


