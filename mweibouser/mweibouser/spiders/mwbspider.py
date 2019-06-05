# -*- coding: utf-8 -*-
from scrapy import Spider,Request
import json
from mweibouser.items import *

class MwbspiderSpider(Spider):
    name = 'mwbspider'
    allowed_domains = ['m.weibo.cn']
    start_urls = ['http://m.weibo.cn/']
    # user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    #
    # follows_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    #
    # fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'
    #
    # weibos_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{uid}_-_WEIBO_SECOND_PROFILE_WEIBO&type=uid&value={uid}&page_type=03&page={page}'
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'

    follows_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'

    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&page={page}'

    weibos_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}'

    start_users = ['3217179555', '1742566624', '2282991915', '1288739185', '3952070245', '5878659096']

    def start_requests(self):
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid),callback=self.parse_user)

    # def parse_user(self, response):
    #
    #     # self.logger.debug('now is user parse' + response.status)
    #
    #     result = json.loads(response.text)
    #     if result.get('data').get('userInfo'):
    #         user_info = result.get('data').get('userInfo')
    #         useritem = UserItem()
    #         # 为了方便动态赋值 制作一个字符串映射map
    #         field_map = {
    #             'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
    #             'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
    #             'follows_count': 'follow_count', 'weibos_count': 'statuses_count', 'verified': 'verified',
    #             'verified_reason': 'verified_reason', 'verified_type': 'verified_type'
    #         }
    #         for field,attr in field_map.items():
    #             useritem[field] = user_info.get(attr)
    #         yield useritem
    #
    #         # 分别返回三种请求
    #         uid = user_info.get('id')
    #         # meta需要传递 从而便于解析函数获取当前uid page 虽然也可以通过url解析得到
    #         yield Request(self.follows_url.format(uid=uid,page=1),callback=self.parse_follows,meta={'page':1,'uid':uid})
    #         yield Request(self.fans_url.format(uid=uid,page=1),callback=self.parse_fans,meta={'uid':uid,'page':1})
    #         yield Request(self.weibos_url.format(uid=uid,page=1),callback=self.parse_weiboconts,meta={'uid':uid,'page':1})
    #
    # def parse_follows(self,response):
    #     '''
    #     三个任务：    用户id从而发起用户请求
    #                 获取用户关系并且存储形成item
    #                 获取下一页进行解析
    #
    #     '''
    #     # self.logger.debug('now is follows parse' + response.status)
    #
    #     result = json.loads(response.text)
    #     # 小心 最后一个才是需要的 因为第一页中最后一条才是他的全部关注中的第一页
    #     if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and result.get('data').get('cards')[-1].get('card_group'):
    #         follows = result.get('data').get('cards')[-1].get('card_group')
    #         for follow in follows:
    #             # 第一个任务
    #             if follow.get('user'):
    #                 uid = follow.get('user').get('id')
    #                 yield Request(self.user_url.format(uid=uid),callback=self.parse_user)
    #         # 第二个任务
    #         uid = response.meta.get('uid')
    #
    #         relationitem = RelationItem()
    #         relationitem['id'] = uid
    #         # 此处仅保留name id字典 使用列表生成式
    #         user_follows = [{'id':follow.get('user').get('id'),'name':follow.get('user').get('screen_name')} for follow in follows]
    #         relationitem['follows'] = user_follows
    #         relationitem['fans'] = []
    #         yield relationitem
    #         # 第三个任务
    #         page = response.meta.get('page') + 1
    #         yield Request(self.follows_url.format(uid=uid, page=page),callback=self.parse_follows, meta={'page': page, 'uid': uid})
    #
    #
    # def parse_fans(self,response):
    #     # self.logger.debug('now is fans parse' + response.status)
    #
    #     result = json.loads(response.text)
    #     # 小心 最后一个才是需要的 因为第一页中最后一条才是他的全部关注中的第一页
    #     if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and \
    #             result.get('data').get('cards')[-1].get('card_group'):
    #         fans = result.get('data').get('cards')[-1].get('card_group')
    #         for fan in fans:
    #             # 第一个任务
    #             if fan.get('user'):
    #                 uid = fan.get('user').get('id')
    #                 yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
    #         # 第二个任务
    #         uid = response.meta.get('uid')
    #
    #         relationitem = RelationItem()
    #         relationitem['id'] = uid
    #         # 此处仅保留name id字典 使用列表生成式
    #         user_fans = [{'id': fan.get('user').get('id'), 'name': fan.get('user').get('screen_name')} for fan in fans]
    #         relationitem['follows'] = []
    #         relationitem['fans'] = user_fans
    #         yield relationitem
    #         # 第三个任务
    #         page = response.meta.get('page') + 1
    #         yield Request(self.fans_url.format(uid=uid, page=page), callback=self.parse_fans,
    #                       meta={'page': page, 'uid': uid})
    #
    # def parse_weiboconts(self,response):
    #     '''
    #     微博详情页解析
    #     两个任务：
    #             得到weiboitem
    #             发起下一页微博信息请求
    #     '''
    #     # self.logger.debug('now is weibo parse' + response.status)
    #     result = json.loads(response.text)
    #     if result.get('ok') and result.get('data').get('cards'):
    #         weibos = result.get('data').get('cards')
    #         for weibo in weibos:
    #             # 有的没有mblog区块 只是开头索引 这个不同于fans等列表 不需要[-1]
    #             mblog = weibo.get('mblog')
    #             if mblog:
    #                 weibo_item = WeiboContItem()
    #                 field_map = {
    #                     'id': 'id', 'attitudes_count': 'attitudes_count', 'comments_count': 'comments_count',
    #                     'reposts_count': 'reposts_count', 'picture': 'original_pic', 'pictures': 'pics',
    #                     'created_at': 'created_at', 'source': 'source', 'text': 'text', 'raw_text': 'raw_text',
    #                     'thumbnail': 'thumbnail_pic',
    #                 }
    #                 for field, attr in field_map.items():
    #                     weibo_item[field] = mblog.get(attr)
    #
    #                 weibo_item['user'] = response.meta.get('uid')
    #                 yield weibo_item
    #
    #         # 下一页微博
    #         uid = response.meta.get('uid')
    #         page = response.meta.get('page') + 1
    #         yield Request(self.weibos_url.format(uid=uid, page=page), callback=self.parse_weiboconts,
    #                       meta={'uid': uid, 'page': page})
    #
    #
    def parse_user(self, response):
        """
        解析用户信息
        :param response: Response对象
        """
        self.logger.debug(response)
        result = json.loads(response.text)
        if result.get('data').get('userInfo'):
            user_info = result.get('data').get('userInfo')
            user_item = UserItem()
            field_map = {
                'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
                'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
                'follows_count': 'follow_count', 'weibos_count': 'statuses_count', 'verified': 'verified',
                'verified_reason': 'verified_reason', 'verified_type': 'verified_type'
            }
            for field, attr in field_map.items():
                user_item[field] = user_info.get(attr)
            yield user_item
            # 关注
            uid = user_info.get('id')
            yield Request(self.follows_url.format(uid=uid, page=1), callback=self.parse_follows,
                          meta={'page': 1, 'uid': uid})
            # 粉丝
            yield Request(self.fans_url.format(uid=uid, page=1), callback=self.parse_fans,
                          meta={'page': 1, 'uid': uid})
            # 微博
            yield Request(self.weibos_url.format(uid=uid, page=1), callback=self.parse_weibos,
                          meta={'page': 1, 'uid': uid})

    def parse_follows(self, response):
        """
        解析用户关注
        :param response: Response对象
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and \
                result.get('data').get('cards')[-1].get(
                        'card_group'):
            # 解析用户
            follows = result.get('data').get('cards')[-1].get('card_group')
            for follow in follows:
                if follow.get('user'):
                    uid = follow.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

            uid = response.meta.get('uid')
            # 关注列表
            user_relation_item = RelationItem()
            follows = [{'id': follow.get('user').get('id'), 'name': follow.get('user').get('screen_name')} for follow in
                       follows]
            user_relation_item['id'] = uid
            user_relation_item['follows'] = follows
            user_relation_item['fans'] = []
            yield user_relation_item
            # 下一页关注
            page = response.meta.get('page') + 1
            yield Request(self.follows_url.format(uid=uid, page=page),
                          callback=self.parse_follows, meta={'page': page, 'uid': uid})

    def parse_fans(self, response):
        """
        解析用户粉丝
        :param response: Response对象
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and \
                result.get('data').get('cards')[-1].get(
                        'card_group'):
            # 解析用户
            fans = result.get('data').get('cards')[-1].get('card_group')
            for fan in fans:
                if fan.get('user'):
                    uid = fan.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

            uid = response.meta.get('uid')
            # 粉丝列表
            user_relation_item = RelationItem()
            fans = [{'id': fan.get('user').get('id'), 'name': fan.get('user').get('screen_name')} for fan in
                    fans]
            user_relation_item['id'] = uid
            user_relation_item['fans'] = fans
            user_relation_item['follows'] = []
            yield user_relation_item
            # 下一页粉丝
            page = response.meta.get('page') + 1
            yield Request(self.fans_url.format(uid=uid, page=page),
                          callback=self.parse_fans, meta={'page': page, 'uid': uid})

    def parse_weibos(self, response):
        """
        解析微博列表
        :param response: Response对象
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards'):
            weibos = result.get('data').get('cards')
            for weibo in weibos:
                mblog = weibo.get('mblog')
                if mblog:
                    weibo_item = WeiboContItem()
                    field_map = {
                        'id': 'id', 'attitudes_count': 'attitudes_count', 'comments_count': 'comments_count',
                        'reposts_count': 'reposts_count', 'picture': 'original_pic', 'pictures': 'pics',
                        'created_at': 'created_at', 'source': 'source', 'text': 'text', 'raw_text': 'raw_text',
                        'thumbnail': 'thumbnail_pic',
                    }
                    for field, attr in field_map.items():
                        weibo_item[field] = mblog.get(attr)
                    weibo_item['user'] = response.meta.get('uid')
                    yield weibo_item
            # 下一页微博
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield Request(self.weibos_url.format(uid=uid, page=page), callback=self.parse_weibos,
                          meta={'uid': uid, 'page': page})