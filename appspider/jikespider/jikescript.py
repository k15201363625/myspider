import json
import pymongo
import re
from config import *
import logging
# from UserInfo import UserInfo
from UserInfo import userinfo
# from urllib.parse import unquote
# 对于列表滚动时的用户信息进行抓取 并且保存到mongoddb中

# client = pymongo.MongoClient(MONGO_HOST)
# db = client[MONGO_DATABASE]
# usertable = db[TABLE_NAME]
class MyMongo:
    def __init__(self):
        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client['jike']
        self.usertable = self.db['userinfo']
    def update_info(self,id,userinfo):
        self.usertable.update({'id': id}, {'$set': userinfo}, True)

# 截取response flow进行处理
def response(flow):
    # global usertable,logger
    logger = logging.getLogger(__name__)

    fansurl = 'https://app.jike.ruguoapp.com/1.0/userRelation/getFollowingList'
    followsurl = 'https://app.jike.ruguoapp.com/1.0/userRelation/getFollowerList'
    # userinfo = UserInfo()
    # attrlist = dir(userinfo)[-15:]

    if (fansurl in flow.request.url) or (followsurl in flow.request.url):
        # 分析当前页面 提取用户信息 
        logger.info("=====================================")
        
        text = flow.response.text
        data = json.loads(text)
        if len(data.get("data")) != 0:
            logger.info("-----------------------------------")
            users = data.get("data")
            for user in users:
                # for attr in attrlist:
                for attr in userinfo.keys():
                    if user.get(attr):
                        userinfo[attr] = user.get(attr)

                id = user.get('id')
                # 存储到mongodb 
                mymongo = MyMongo()
                mymongo.update_info(id,userinfo)
                logger.info("saved mongodb id is:",id)
