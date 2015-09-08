# Scrapy settings for xueqiu project

SPIDER_MODULES = ['xueqiu.spiders']
NEWSPIDER_MODULE = 'xueqiu.spiders'
DEFAULT_ITEM_CLASS = 'xueqiu.items.Website'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'

ITEM_PIPELINES = ['xueqiu.pipelines.MongoDBPipeline']

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "xueqiu"
MONGODB_COLLECTION = "vperson"

MONGODB_COLLECTION_MEMBERS = "members"