from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest

from xueqiu.items import personalCubes,personalQuote,VPerson

import json
import time


class xueqiu(Spider):
    name = "xueqiu"
    allowed_domains = ["xueqiu.com"]
    start_urls = [
        "http://xueqiu.com/3721302206"
    ]
    vPerson = VPerson()
    counter = 0

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://xueqiu.com
        @scrapes name
        """
        
        sel = Selector(response)
        self.user_id = sel.css('h2 .setRemark::attr(data-user-id)').extract()
        # get cubes
        yield FormRequest('http://xueqiu.com/cubes/list.json',
         callback=self.cubes,
         method='get',
         formdata={
         'user_id': self.user_id, 
         'count': '100',
         '_': str(int(time.time()))
         })

        #get stocks
        yield FormRequest('http://xueqiu.com/stock/portfolio/stocks.json',
         callback=self.getQuote,
         method='get',
         formdata={
         'size': '1000', 
         'tuid': self.user_id,
         '_': str(int(time.time()))
         })

        #top status
        yield FormRequest('http://xueqiu.com/user/top_status_count_stock.json',
         callback=self.topStatusStock,
         method='get',
         formdata={
         'count': '5', 
         'uid': self.user_id,
         '_': str(int(time.time()))
         })

    def cubes(self, response):
        self.vPerson['cubesList'] = json.loads(response.body)['list']
        self.counter = self.counter+1
        if self.counter == 3:
            self.vPerson['user_id'] = self.user_id[0]
            yield self.vPerson

    def getQuote(self, response):
        code = ''
        for stock in json.loads(response.body)['stocks']:
            code = code + str(stock['code']) + ','
            print code
        yield FormRequest('http://xueqiu.com/stock/quote.json',
         callback=self.quote,
         method='get',
         formdata={
         'code': code, 
         '_': str(int(time.time()))
         })

    def quote(self, response):
        self.vPerson['quotesList'] = json.loads(response.body)['quotes']
        self.counter = self.counter+1
        if self.counter == 3:
            self.vPerson['user_id'] = self.user_id[0]
            yield self.vPerson

    def topStatusStock(self, response):
        self.vPerson['topStatus'] = json.loads(response.body)
        self.counter = self.counter+1
        if self.counter == 3:
            self.vPerson['user_id'] = self.user_id[0]
            yield self.vPerson


