# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

class ProxyMiddleware(object):
    def get_proxy(self):
        try:
            response = requests.get('http://localhost:5555/random')
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    def process_response(self, request, response, spider):
        response.status_code = 200
        return response


    def process_exception(self, request, exception, spider):
        proxy = self.get_proxy()
        print('Using ...')
        request = request.meta['proxy'] = proxy
        return request