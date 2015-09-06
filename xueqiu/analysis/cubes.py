import pymongo

from scrapy.conf import settings
from bson.code import Code

connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT']) 
db = connection[settings['MONGODB_DB']]
collection = db[settings['MONGODB_COLLECTION']]
mapper = Code("""
	function () {
		this.cubesList.forEach(function(z){
			var value = {
				total_gain: z.total_gain,
				daily_gain: z.daily_gain,
				monthly_gain: z.monthly_gain,
				annualized_gain_rate: z.annualized_gain_rate
			}
			emit(z['owner_id'], value);
		});
	}
	""")
reducer = Code("""
	function (key, values) {
		var total = {
			total_gain: 0,
			daily_gain: 0,
			monthly_gain: 0,
			annualized_gain_rate: 0
		};
		for (var i = 0; i < values.length; i++) {
			total.total_gain += values[i].total_gain/values.length;
			total.daily_gain += values[i].daily_gain/values.length;
			total.monthly_gain += values[i].monthly_gain/values.length;
			total.annualized_gain_rate += values[i].annualized_gain_rate/values.length;
		}
		return total;
	}
	""")
result = collection.map_reduce(mapper, reducer, "cubes")