import pymongo
from scrapy.conf import settings
from bson.code import Code


connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT']) 
db = connection[settings['MONGODB_DB']]
vpersons = db[settings['MONGODB_COLLECTION']]

status = db['status']
status.remove()
for vperson in vpersons.find():
	stockInfo = {'score': 0}
	for stockInfo in vperson['topStatus']:
		print stockInfo
	status.insert_one({'user_id':vperson['user_id'],'score':stockInfo['score']});
