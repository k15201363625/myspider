# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# imatate docs of scrapy

import pymongo

class MongoPipeLine(object):

    def __init__(self,mongo_uri,mongo_db,table_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.table_name = table_name

    @classmethod
    def from_crawler(cls,clawer):
        return cls(
            mongo_db=clawer.settings.get('MONGO_DB'),
            mongo_uri=clawer.settings.get('MONGO_URI'),
            table_name=clawer.settings.get('TABLE_NAME')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item,spider):
        # 使用条件更新 去重
        self.db[self.table_name].update({'url_token':item['url_token']},dict(item),True)
        return item

    def close_spider(self,spider):
        self.client.close()


