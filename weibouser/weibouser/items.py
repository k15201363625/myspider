# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


# 由于有不同的item保存在一个数据库的不同表中 所以表明在item中定义
class WeiboContItem(Item):
    item_table_name = 'weibo_cont'

    id = Field()
    content = Field()
    posted_time = Field()
    url = Field()
    user = Field()
    crawled_at = Field()
    forward_count = Field()
    comment_count = Field()
    like_count = Field()

