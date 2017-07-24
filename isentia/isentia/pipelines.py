# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy import log

class IsentiaPipeline(object):
    def __init__(self):
        self._connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self._db = self._connection[settings['MONGODB_DB']]
        self._collection = self._db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if item:
            self._collection.insert(dict(item))
            log.msg("Article added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
