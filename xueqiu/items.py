from scrapy.item import Item, Field

class Weibos(Item):
	user_id = Field()
	weibosList = Field()
	symbols = Field()

class VPerson(Item):
	user_id = Field()
	cubesList = Field()
	quotesList = Field()
	topStatus = Field()

class Members(Item):
	user_id = Field()
	followers_count = Field()
	user_name = Field()
