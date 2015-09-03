# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'

ITEM_PIPELINES = ['dirbot.pipelines.MongoDBPipeline', ]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "xueqiu"
MONGODB_COLLECTION = "vperson"