# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymongo
import re
from weibouser.items import WeiboContItem

# 爬取内容清洗
class WeibouserPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item,WeiboContItem):
            # 对于内容时间进行修正
            if item.get('content'):
                item['content'] = item['content'].lstrip(':').strip()
            if item.get('posted_time'):
                item['posted_time'] = item['posted_time'].strip()
                item['posted_time'] = self.parse_time(item['posted_time'])
        return item

    def parse_time(self, datetime):
        # 一小时内
        if re.match('\d+分钟前', datetime):
            minute = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y年%m月%d日 %H:%M', time.localtime(time.time() - float(minute) * 60))
        # 当天
        if re.match('今天.*', datetime):
            datetime = re.match('今天(.*)', datetime).group(1).strip()
            datetime = time.strftime('%Y年%m月%d日', time.localtime()) + ' ' + datetime
        # 非当天
        if re.match('\d+月\d+日', datetime):
            datetime = time.strftime('%Y年', time.localtime()) + datetime
        return datetime

# 爬取内容保存
class MongoPipline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        # 使用mongodb更新方式 redis也有这样的方式
        self.db[item.item_table_name].update({'id':item.get('id')},{'$set':dict(item)},True)
        return item





