# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymongo
import re
from mweibouser.items import *


# 对于user  以及 weibo item加上爬起时间字段
class TimePipeLine(object):
    def process_item(self, item, spider):
        if isinstance(item, UserItem) or isinstance(item, WeiboContItem):
            nowtime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            item['crawled_at'] = nowtime
        return item

# 对于weibo中已有的time字段进行格式化
class FormatTimePipeLine(object):
    def parse_time(self, date):
        if re.match('刚刚', date):
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        if re.match('\d+分钟前', date):
            minute = re.match('(\d+)', date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+小时前', date):
            hour = re.match('(\d+)', date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('昨天.*', date):
            date = re.match('昨天(.*)', date).group(1).strip()
            date = time.strftime('%Y-%m-%d', time.localtime() - 24 * 60 * 60) + ' ' + date
        if re.match('\d{2}-\d{2}', date):
            date = time.strftime('%Y-', time.localtime()) + date + ' 00:00'
        return date

    def process_item(self, item, spider):
        if isinstance(item, WeiboContItem):
            if item.get('created_at'):
                item['created_at'] = item['created_at'].strip()
                item['created_at'] = self.parse_time(item.get('created_at'))
            if item.get('pictures'):
                # 对于图片信息 单独处理 picurl 保存成列表形式
                item['pictures'] = [pic.get('url') for pic in item.get('pictures')]
        return item


class MongoPipeLine(object):
    # 处理关系列表是关键 合并到user信息中
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        # 创建链接 + 由于需要大量插入更新去重 以及通过查询添加粉丝关注列表
        # 所以需要建立索引 加快查询速度 而使用唯一的id字段建立索引
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # 通过元祖列表 远足中制定key/字段 以及 direction方向
        self.db[UserItem.collection].create_index([('id',pymongo.ASCENDING)])
        self.db[WeiboContItem.collection].create_index([('id',pymongo.ASCENDING)])

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        '''
        处理更新重点
        [1] 对于user weibocont item直接更新即可
        [2] 对于relationItem对象 需要使用 addtoset方式插入到已有的user数据中 作为列表形式存储的独立字段
        '''
        if isinstance(item,UserItem) or isinstance(item,WeiboContItem):
            # True制定不存在时插入 set也很重要 制定存在的时候使用更新而不是覆盖
            self.db[item.collection].update({'id':item.get('id')},{'$set':item},True)
        elif isinstance(item,RelationItem):
            # 使用addtoset方式添加
            # 对于列表型数据 由于内部以字典形式 为了字段对应存储 制定each
            # by germey
            self.db[item.collection].update(
                {'id':item.get('id')},
                {
                    '$addToSet':{
                        'follows':{'$each':item['follows']},
                        'fans':{'$each':item['fans']}
                    }
                },True)
        return item