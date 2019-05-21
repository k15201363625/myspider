# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import json
import requests
from requests import ConnectionError
import logging

# belong to downloadmiddleware
from scrapy.exceptions import IgnoreRequest


class CookiesMiddleware(object):
    def __init__(self,cookiespool_url):
        # 定义log对象 设置setting中的cookiesurl
        self.logger = logging.getLogger(__name__)
        self.cookiespool_url = cookiespool_url

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            cookiespool_url = crawler.settings.get('COOKIESPOOL_URL')
        )

    def _get_random_cookie(self):
        try:
            response = requests.get(self.cookiespool_url)
            if response.status_code == 200:
                return json.loads(response.text)
        except ConnectionError:
            return None

    def process_request(self,request,spider):
        cookie = self._get_random_cookie()
        if cookie:
            request.cookies = cookie
            self.logger.debug('using cookies:'+json.dumps(cookie))
        else:
            self.logger.debug('No available cookies')

    # 处理响应为非正常页面---跳转-> 封号 登录两种页面
    # 解决方法： 更换cookies重试
    def process_response(self, request, response, spider):
        if response.status in [300, 301, 302, 303]:
            try:
                redirect_url = response.headers['location']
                if 'login.weibo' in redirect_url or 'login.sina' in redirect_url:
                    # Cookie失效
                    self.logger.warning('Updating Cookies')
                elif 'weibo.cn/security' in redirect_url:
                    # 封号
                    self.logger.warning('Now Cookies is locked:' + json.dumps(request.cookies))
                    self.logger.warning('One Account is locked!')
                # 解决方案
                request.cookies = self._get_random_cookie()
                self.logger.debug('Using Cookies' + json.dumps(request.cookies))
                return request

            except Exception:
                raise IgnoreRequest
        # 重新请求
        elif response.status in [414]:
            return request
        else:
            return response
class StopCrawlException(Exception):
    def __repr__(self):
        return str(self.reason)


class WeibouserDownloaderMiddleware(object):
    def process_response(self, request, response, spider):
        if response.status in [300, 301, 302, 303]:
            try:
                redirect_url = response.url
                if 'passport.weibo.cn' in redirect_url:
                    self.logger.warning('Now Cookies is unavailable:' + json.dumps(request.cookies))
                elif 'weibo.cn/security' in redirect_url:
                    # 封号
                    self.logger.warning('Now Cookies is locked:' + json.dumps(request.cookies))
                    self.logger.warning('One Account is locked!')
                # 解决方案
                raise StopCrawlException('stop crawl because unavailable cookie')
            except Exception:
                raise IgnoreRequest
        # 重新请求
        elif response.status in [414]:
            return request
        else:
            return response


'''
class WeibouserSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeibouserDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

'''