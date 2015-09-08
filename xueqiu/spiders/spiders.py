from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import FormRequest
from scrapy.conf import settings

from xueqiu.items import VPerson, Members, Weibos

import json
import re
import math
import time

import pymongo


class xueqiu(Spider):
    name = "xueqiu"
    allowed_domains = ["xueqiu.com"]
    
    connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT']) 
    db = connection[settings['MONGODB_DB']]
    memberCollection = db[settings['MONGODB_COLLECTION_MEMBERS']]
    vpersonCollection = db[settings['MONGODB_COLLECTION']]
    menbers =  memberCollection.find()
    
    start_urls = []
    vPersons = {}

    for menber in menbers:
        if vpersonCollection.find({'user_id':menber['user_id']}).count() != 0:
            continue
        start_urls.append("http://xueqiu.com/"+menber['user_id'])
        vPersons[menber['user_id']] = VPerson()
        vPersons[menber['user_id']]['user_id'] = menber['user_id']


    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://xueqiu.com
        @scrapes name
        """
        
        sel = Selector(response)
        user_id = sel.css('h2 .setRemark::attr(data-user-id)').extract()
        # get cubes
        yield FormRequest('http://xueqiu.com/cubes/list.json',
         callback=self.cubes,
         method='get',
         formdata={
         'user_id': user_id, 
         'count': '100',
         '_': str(int(time.time()))
         })

        # get stocks
        yield FormRequest('http://xueqiu.com/stock/portfolio/stocks.json',
         callback=self.getQuote,
         method='get',
         formdata={
         'size': '1000', 
         'tuid': user_id,
         '_': str(int(time.time()))
         })

        # top status
        yield FormRequest('http://xueqiu.com/user/top_status_count_stock.json',
         callback=self.topStatusStock,
         method='get',
         formdata={
         'count': '5', 
         'uid': user_id,
         '_': str(int(time.time()))
         })

    def isFull(self, tgt):
        if 'cubesList' not in tgt:
            return False
        if 'quotesList' not in tgt:
            return False
        if 'topStatus' not in tgt:
            return False
        return True

    def cubes(self, response):
        uid = str(re.search(r'user_id=(\d+)',
            response.request.url).group(1))
        self.vPersons[uid]['cubesList'] = json.loads(response.body)['list']
        print self.isFull(self.vPersons[uid]),self.vPersons[uid]
        if self.isFull(self.vPersons[uid]):
            yield self.vPersons[uid]


    def getQuote(self, response):
        def quote(res):
            self.vPersons[uid]['quotesList'] = json.loads(res.body)['quotes']
            if self.isFull(self.vPersons[uid]):
                yield self.vPersons[uid]
        code = ''
        uid = str(re.search(r'tuid=(\d+)',response.request.url).group(1))
        for stock in json.loads(response.body)['stocks']:
            code = code + str(stock['code']) + ','
            if len(code) > 200:
                break
        yield FormRequest('http://xueqiu.com/stock/quote.json',
         callback=quote,
         method='get',
         formdata={
         'code': code, 
         '_': str(int(time.time()))
         })

    def topStatusStock(self, response):
        uid = str(re.search(r'uid=(\d+)',
            response.request.url).group(1))
        self.vPersons[uid]['topStatus'] = json.loads(response.body)
        if self.isFull(self.vPersons[uid]):
            yield self.vPersons[uid]
class members(Spider):
    name = "members"
    allowed_domains = ["xueqiu.com"]
    start_urls = [
        "http://xueqiu.com/7730004385"
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
        followNum = int(re.findall(r'\d+', sel.css('ul.nav.nav-tabs li:nth-child(3) a::text').extract()[1])[0])
        maxPage = int(math.ceil(followNum/20.0))
        print maxPage

        for index in range(maxPage):
            yield FormRequest('http://xueqiu.com/friendships/groups/members.json',
             callback=self.saveMember,
             method='get',
             formdata={
             'uid': self.user_id, 
             'gid': '0', 
             'page': str(index),
             '_': str(int(time.time()))
             })    
        
        

    def saveMember(self, response):
        members = json.loads(response.body)['users']
        for member in members:
            if member['followers_count'] < 10000: 
                continue
            m = Members()
            m['user_id'] = str(member['id'])
            m['followers_count'] = member['followers_count']
            m['user_name'] = member['screen_name']
            yield m
            for index in range(int(member['friends_count']/20)):
                yield FormRequest('http://xueqiu.com/friendships/groups/members.json',
                         callback=self.saveMember,
                         method='get',
                         formdata={
                         'uid': str(member['id']), 
                         'gid': '0', 
                         'page': str(index),
                         '_': str(int(time.time()))
                         })

class weibos(Spider):
    name = "weibos"
    allowed_domains = ["xueqiu.com"]
    
    connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT']) 
    db = connection[settings['MONGODB_DB']]
    vpersonCollection = db[settings['MONGODB_COLLECTION']]
    vPersons =  vpersonCollection.find()
    
    start_urls = []
    weibosHash = {}

    for vPerson in vPersons:
        symbols = []
        uid = str(vPerson['user_id'])
        for symbol in vPerson['topStatus']:
            symbols.append(symbol['symbol'])
        start_urls.append("http://xueqiu.com/"+vPerson['user_id'])
        weibosHash[uid] = Weibos()
        weibosHash[uid]['user_id'] = uid
        weibosHash[uid]['symbols'] = symbols
        weibosHash[uid]['weibosList'] = []


    print weibosHash
    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://xueqiu.com
        @scrapes name
        """
        
        sel = Selector(response)
        user_id = sel.css('h2 .setRemark::attr(data-user-id)').extract()[0]
        # get weibo
        for symbol in self.weibosHash[str(user_id)]['symbols']:
            yield FormRequest('http://xueqiu.com/statuses/search.json',
             callback=self.stocksWeibo,
             method='get',
             formdata={
             'uid': user_id, 
             'symbol': symbol,
             'page': '1',
             'ex': '1',
             'sort': 'time',
             'comment': '0',
             '_': str(int(time.time()))
             })

    def stocksWeibo(self, response):
        uid = str(re.search(r'uid=(\d+)',
            response.request.url).group(1))
        symbol = str(re.search(r'symbol=(.+?)&',
            response.request.url).group(1))
        print symbol
        self.weibosHash[uid]['weibosList'].append({'symbol':symbol, 'list':json.loads(response.body)['list']})
        if len(self.weibosHash[uid]['symbols']) <= len(self.weibosHash[uid]['weibosList']):
            yield self.weibosHash[uid]
