from scrapy.item import Item, Field


class StackItem(Item):
    title = Field()
    url = Field()

class personalCubes(Item):
	list = Field()
	user_id = Field()

class personalQuote(Item):
	quotes = Field()
	user_id = Field()

class VPerson(Item):
	user_id = Field()
	cubesList = Field()
	quotesList = Field()
	topStatus = Field()

class Weibo(Item):
	user_id = Field()
	weibosList = Field()