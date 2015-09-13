import pymongo
from scrapy.conf import settings
import time
import requests
import json

'''
Get 3 periods' trust diff between the timePeriod list's timestamp 
'''
def getTrust(symbol):
	timePeriod = [1433088000000,1435680000000,1438272000000,1441036800000]
	url = 'http://xueqiu.com/cubes/nav_daily/all.json'
	user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
	values = {'cube_symbol': symbol}
	cookies = dict(s='vkw1jeg9ks',xq_a_token='f358ee5c611a2205af323bf15022b2df7e2ca272',xq_r_token='55ae3036fe097ecbb1ffc11bd31b867ef88ce358',__utma='1.250806624.1441870600.1441870600.1441876620.2', __utmb='1.12.10.1441876620', __utmc='1', __utmz='1.1441870600.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',Hm_lvt_1db88642e346389874251b5a1eded6e3='1441801836,1441850892', Hm_lpvt_1db88642e346389874251b5a1eded6e3='1441877622')
	results = requests.get(url,
	              params=values,
	              headers={'User-Agent': user_agent}, cookies=cookies)
	trustValues = {}
	try:
		cvalues = {}
		rlist = results.json()[0]['list']
		for r in rlist:
			if r['time'] == timePeriod[0]:
				cvalues['a'] = r['percent']
			if r['time'] == timePeriod[1]:
				cvalues['b'] = r['percent']
			if r['time'] == timePeriod[2]:
				cvalues['c'] = r['percent']
			if r['time'] == timePeriod[3]:
				cvalues['d'] = r['percent']
		if  cvalues.has_key('a') and cvalues.has_key('b'):
			trustValues['m1'] = cvalues['b']-cvalues['a']
		if  cvalues.has_key('b') and cvalues.has_key('c'):
			trustValues['m2'] = cvalues['c']-cvalues['b']
		if  cvalues.has_key('c') and cvalues.has_key('d'):
			trustValues['m3'] = cvalues['d']-cvalues['c']
		return trustValues
	except Exception, e:
		print e
		return 0

def calmonth(trusts, m):
	monthsum = 0
	i = 0
	for trust in trusts:
		if trust.has_key(m):
			monthsum += trust[m]
			i = i + 1
	if i !=0:
		return monthsum/i
	else:
		return 'null'

def main():
	connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT']) 
	db = connection[settings['MONGODB_DB']]

	vpersons = db[settings['MONGODB_COLLECTION']]
	cubesmonth = db['cubesmonth']
	members = db['members']
	cubesmonth.remove()
	for vperson in vpersons.find():
		cubes_num = len(vperson['cubesList'])
		member = members.find_one({'user_id':vperson['user_id']})
		nickname = member['user_name']
		if(cubes_num==0):
			cubesmonth.insert_one({'user_id':vperson['user_id'],'nickname': nickname ,'m1':'null','m2':'null','m3':'null'});
			continue
		trusts = []
		for cubeInfo in vperson['cubesList']:
			trusts.append(getTrust(cubeInfo['symbol']))
		m1 = calmonth(trusts, 'm1')
		m2 = calmonth(trusts, 'm2')
		m3 = calmonth(trusts, 'm3')
		cubesmonth.insert_one({'user_id':vperson['user_id'],'nickname': nickname ,'m1':m1,'m2':m2,'m3':m3});
 
if __name__ == "__main__":
    main();
