import pymongo
from scrapy.conf import settings
from bson.code import Code

'''
A script to analyse cubes info
store [total_gain,daily_gain,monthly_gain,annualized_gain_rate] into db['cubes'] collection
'''
connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT']) 
db = connection[settings['MONGODB_DB']]

vpersons = db[settings['MONGODB_COLLECTION']]
cubes = db['cubes']
members = db['members']
cubes.remove()
for vperson in vpersons.find():
	(total_gain, daily_gain, monthly_gain, annualized_gain_rate) = (0, 0, 0, 0)
	cubes_num = len(vperson['cubesList'])
	if(cubes_num==0):
		member = members.find_one({'user_id':vperson['user_id']})
		nickname = member['user_name']
		cubes.insert_one({'user_id':vperson['user_id'],'nickname': nickname ,'total_gain':'null','daily_gain':'null','monthly_gain':'null','annualized_gain_rate':'null'});
		continue
	nickname =''
	for cubeInfo in vperson['cubesList']:
		total_gain += cubeInfo['total_gain'] / cubes_num
		daily_gain += cubeInfo['daily_gain'] / cubes_num
		monthly_gain += cubeInfo['monthly_gain'] / cubes_num
		annualized_gain_rate += cubeInfo['annualized_gain_rate'] / cubes_num
		nickname = cubeInfo['owner']['screen_name']
	if not nickname:
		member = members.find_one({'user_id':vperson['user_id']})
		nickname = member['user_name']
	cubes.insert_one({'user_id':vperson['user_id'],'nickname': nickname ,'total_gain':total_gain,'daily_gain':daily_gain,'monthly_gain':monthly_gain,'annualized_gain_rate':annualized_gain_rate});
