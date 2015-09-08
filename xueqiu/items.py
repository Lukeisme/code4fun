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

<<<<<<< HEAD
class Weibo(Item):
	user_id = Field()
	weibosList = Field()
=======
class Members(Item):
	user_id = Field()
	followers_count = Field()
	user_name = Field()
>>>>>>> 09bcc1835fc6dfc7a7813662a04d5a2ccd21f296
