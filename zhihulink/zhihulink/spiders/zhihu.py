# -*- coding: utf-8 -*-

from scrapy import Spider,Request
from zhihulink.items import UserItem
import json

class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followees_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'


    start_user = 'stormzhang'

    def start_requests(self):
        # url = 'https://www.zhihu.com/api/v4/members/Germey?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
        # url = 'https://www.zhihu.com/api/v4/members/Germey/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
        yield Request(self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        # yield Request(self.followers_url.format(user=self.start_user,include=self.followers_query,offset=0,limit=20),callback=self.parse_followers)


    def parse_user(self, response):
        res = json.loads(response.text)
        useritem = UserItem()
        for field in useritem.fields:
            if field in res.keys():
                useritem[field] = res.get(field)
        yield useritem
        yield Request(self.followers_url.format(user=res.get('url_token'),include=self.followers_query,offset=0,limit=20),callback=self.parse_followers)
        yield Request(self.followees_url.format(user=res.get('url_token'),include=self.followees_query,offset=0,limit=20),callback=self.parse_followees)






    def parse_followers(self,response):
        res = json.loads(response.text)
        if 'data' in res.keys():
            for follower in res.get('data'):
                yield Request(self.user_url.format(user=follower.get('url_token'),include=self.user_query),callback=self.parse_user)

        if 'paging' in res.keys():
            if res.get('paging').get('is_end') == False:
                next_page = res.get('paging').get('next')
                yield Request(next_page,callback=self.parse_followers)


    def parse_followees(self,response):
        res = json.loads(response.text)
        if 'data' in res.keys():
            for follower in res.get('data'):
                yield Request(self.user_url.format(user=follower.get('url_token'),include=self.user_query),callback=self.parse_user)

        if 'paging' in res.keys():
            if res.get('paging').get('is_end') == False:
                next_page = res.get('paging').get('next')
                yield Request(next_page,callback=self.parse_followees)