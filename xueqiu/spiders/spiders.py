from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest

from dirbot.items import StackItem

import json


class xueqiu(Spider):
    name = "xueqiu"
    allowed_domains = ["xueqiu.com"]
    start_urls = [
        "http://xueqiu.com/3721302206"
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://xueqiu.com
        @scrapes name
        """
        # sel = Selector(response)
        # sites = sel.css('table')
        # items = []

        # for site in sites:
        #     item = tableHeader()
        #     item['head'] = site.css('th::text').extract()
        #     items.append(item)
        yield FormRequest('http://xueqiu.com/cubes/list.json?user_id=3721302206&count=20&_=1441268521824',
         callback=self.cubes,
         method='get',
         formdata={
         'user_id': '3721302206', 
         'count': '100',
         '_':'1441268521824'
         })

    def cubes(self, response):
        # json_file = response.body.count
        print json.loads(response.body)['count']


class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]/h3')

        for question in questions:
            item = StackItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            yield item