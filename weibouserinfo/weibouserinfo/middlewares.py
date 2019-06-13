# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from requests import ConnectionError
import requests
import json
import logging
# Spider自带logger 但是在其他部分需要自己生成logger



class CookiesMiddleWare(object):
    def __init__(self, cookies_url):
        self.logger = logging.getLogger(__name__)
        self.cookies_url = cookies_url

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            cookies_url=settings.get('COOKIES_URL')
        )

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies = json.loads(response.text)
                return cookies
        except ConnectionError:
            return False

    def process_request(self,request,spider):
        self.logger.debug('-------getting cookies-----')
        cookies = self.get_random_cookies()
        if cookies:
            # 直接设置cookies字段即可
            request.cookies = cookies
            self.logger.debug('using cookies ' + json.dumps(cookies))

    def process_response(self,request,response,spider):
        # 暂时不做处理 后续补充对于异常页面切换cookies
        # 从而保证信息的完整不缺失 否则那个页面就缺失了
        return response



class ProxiesMiddleWare(object):
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except ConnectionError:
            return False

    def process_request(self, request, spider):
        # 由于代理还可以用 不需要平凡切换 所以只有有过出错记录再切换代理
        # 微博封ip不是很严重 不需要一直更换 请求接口本身没有采用异步方式速度较慢
        self.logger.debug('-------getting proxy-----')

        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('using proxy:' + proxy)
                # 通过设定request的meta中的proxy字段 可以使scrapy使用代理请求
                request.meta['proxy'] = uri
    # process_response 目前尚未实现


