'''
A script to analyze the weibos info of the V person
'''
import pymongo
import time
from scrapy.conf import settings
import requests
import json

'''
timePeriod: Vperson 's focus period
symbol: stock symbol
this method calculates the correlation between the focus of vperson and the price fo stock
'''
def getTrust(timePeriod, symbol):
	print timePeriod
	url = 'http://xueqiu.com/stock/forchart/stocklist.json'
	user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
	values = {'symbol': symbol, 'period': 'all', '_': str(int(time.time()))}
	cookies = dict(s='vkw1jeg9ks',xq_a_token='bfba18d152738d946e5d73b0b858eb8be82504eb',xq_r_token='84f0446f8e9268015fe6354226e3660b2f1e4352', _sid='4lTc7eDDORf3vRly9MkCpPv12QQwO1')
	results = requests.get(url,
	              params=values,
	              headers={'User-Agent': user_agent}, cookies=cookies)
	print results
	trustValues = []
	try:
		rlist = results.json()['chartlist']
	except Exception, e:
		print 'wrong cookies'
		return 0
	
	print 'start search'
	fstart = 0
	fend = 0
	for i in range(len(rlist)-1):
		if len(timePeriod) == 0:
			break;
		rlist[i]['time'] = rlist[i]['time'][:-10]+'+0800 '+rlist[i]['time'][-4:]
		rlist[i+1]['time'] = rlist[i]['time'][:-10]+'+0800 '+rlist[i+1]['time'][-4:]
		timetemp = int(time.mktime(time.strptime(rlist[i]['time'], '%a %b %d %H:%M:%S +0800 %Y')))
		timetempNext = int(time.mktime(time.strptime(rlist[i+1]['time'], '%a %b %d %H:%M:%S +0800 %Y')))
		if (timetemp <= timePeriod[0][0]) and (timetempNext > timePeriod[0][0]):
			fstart = timetemp
			pstart = rlist[i]['current']
			print 'findstartTime: %s' % time.strftime('%Y%m%d',time.localtime(timetemp))
		if (timetemp < timePeriod[0][1]) and (timetempNext >= timePeriod[0][1]):
			fend = timetempNext
			pend = rlist[i+1]['current']
			print 'findendTime: %s' % time.strftime('%Y%m%d',time.localtime(timetempNext))
			try :
				val = float(timePeriod[0][1]-timePeriod[0][0])/(fend-fstart)*(pend-pstart)
			except :
				break
			else :
				trustValues.append(float(timePeriod[0][1]-timePeriod[0][0])/(fend-fstart)*(pend-pstart))
			timePeriod.pop(0)
	if(len(trustValues)==0):
		return 0
	else:
		return sum(trustValues)/len(trustValues)

'''
store the results of analysis in 'weibosvalue' collection 
'''
def main():
	connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT']) 
	db = connection[settings['MONGODB_DB']]
	weibosvalue =db['weibosvalue']
	weibosvalue.remove()
	weibos = db[settings['MONGODB_COLLECTION_WEIBOS']]
	members = db['members']
	excludesym = ['SH000001','SZ399001','HKHSI','DJI30','SZ399006','QQQ']
	for person in weibos.find():
		trustValues = []
		for perStock in person['weibosList']:
			print perStock['symbol']
			if perStock['symbol'] in excludesym:
				print perStock['symbol']
				continue
			startTime = None
			endTime = None
			timePeriod = []
			perStock['list'].reverse()
			if(len(perStock['list'])==0):
				continue
			for i in range(len(perStock['list'])):
				if i == 0:
					startTime = perStock['list'][0]['created_at']
					endTime = None
				else:
					if (perStock['list'][i]['created_at'] - perStock['list'][i-1]['created_at'] < 2592000000):
						endTime = perStock['list'][i]['created_at']
					else:
						if not (endTime is None):
							print 'startTime: %s' % time.strftime('%Y%m%d',time.localtime(startTime/1000))
							print 'endTime: %s' % time.strftime('%Y%m%d',time.localtime(endTime/1000))
							timePeriod.append([int(startTime/1000),int(endTime/1000)])
						startTime = perStock['list'][i]['created_at']
						endTime = None
			trustValues.append(getTrust(timePeriod, perStock['symbol']))
		member = members.find_one({'user_id':person['user_id']})
		nickname = member['user_name']
		weibosvalue.insert_one({'user_id':person['user_id'],'nickname': nickname,'trust': sum(trustValues)});

if __name__ == "__main__":
    main();

