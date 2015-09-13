import pymongo
from scrapy.conf import settings
import time
import requests
import json

startNo = 13
def getStatus(symbol, uid):
	results = []
	(num, maxNum) = (1, 1)
	while num <= maxNum:
		time.sleep(1.5)
		url = 'http://xueqiu.com/statuses/search.json'
		user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
		values = {'symbol': symbol,
		'page': str(num),
		'ex': '1',
		'uid': uid,
		'sort':'time',
		'comment':'0',
		'_': str(int(time.time()))
		}
		cookies = dict(s='vkw1jeg9ks',xq_a_token='bfba18d152738d946e5d73b0b858eb8be82504eb',xq_r_token='84f0446f8e9268015fe6354226e3660b2f1e4352')
		res = requests.get(url,
		              params=values,
		              headers={'User-Agent': user_agent}, cookies=cookies)
		print res.content
		try:
			results += res.json()['list']
			maxNum = res.json()['maxPage']
			num = num + 1
		except Exception, e:
			print e
			time.sleep(10)
			break
		
	return results

def main():
	connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT']) 
	db = connection[settings['MONGODB_DB']]
	vpersons = db[settings['MONGODB_COLLECTION']]
	weibos = db['weibos']
	for vperson in vpersons.find().skip(startNo):
		if weibos.find({'user_id':vperson['user_id']}).count() != 0:
			continue
		if len(vperson['topStatus'])==0:
			continue
		weibosList = []
		for status in vperson['topStatus']:
			statusList = getStatus(status['symbol'], status['uid'])
			weibosList.append({'symbol':status['symbol'],'list':statusList})
		weibos.insert_one({'user_id':vperson['user_id'],'weibosList':weibosList})
	
if __name__ == "__main__":
    main();


