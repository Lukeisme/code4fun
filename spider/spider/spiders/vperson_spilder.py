import scrapy
from spider.items import vPersonItem

class vPersonSpider(scrapy.Spider):
	name = "vperson"
	allowed_domains = ['xueqiu.com']
	start_urls =[
		"http://xueqiu.com/7626392721",
		"http://xueqiu.com/8143619147"
	]
	def parse(self, response):
		comb = response.xpath('//tbody')
		for sel in comb.xpath('//td'):
			print sel.extract()


		