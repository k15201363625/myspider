# -*- coding: utf-8 -*-
from scrapy import Spider, FormRequest, Request
import logging

from weibouser.items import WeiboContItem


class WeibospiderSpider(Spider):
    name = 'weibospider'
    allowed_domains = ['weibo.cn']
    start_urls = ['https://weibo.cn/']
    search_url = 'https://weibo.cn/search/mblog'
    max_page = 100

    logger = logging.getLogger(__name__)
    keywords = ['000001']
    # def __init__(self):
    #     # Spider.__init__(self)
    #     super(WeibospiderSpider,self).__init__()

    # 通过post跳页接口得到索引页
    def start_requests(self):
        for keyword in self.keywords:
            url = '{url}?keyword={keyword}'.format(url=self.search_url,keyword=keyword)
            for i in range(self.max_page+1):
                data = {
                    'mp': str(self.max_page),
                    'page': str(i)
                }
                yield FormRequest(url,callback=self.parse_index,formdata=data)
    # 对于索引页解析 得到微博详情页
    # 对于转发微博使用原文链接跳转到原文
    def parse_index(self, response):
        many_weibos = response.xpath('//div[@class="c" and contains(@id,"M_")]')
        self.logger.debug('count of weibos on now page: '+ str(len(many_weibos)))

        is_forward = False
        for weibo in many_weibos:
            is_forward = bool(weibo.xpath('.//span[@class="cmt"]').extract_first())
            if is_forward:
                detail_page_url = weibo.xpath('.//a[contains(.,"原文评论[")]//@href').extract_first()
            else:
                detail_page_url = weibo.xpath('.//a[contains(.,"评论[")]//@href').extract_first()
            yield Request(detail_page_url,callback=self.parse_detail)

    # 对于微博评论详情页进行解析---每个微博有独立的id 但是可能有多个uid
    def parse_detail(self,response):
        url = response.url
        cont_selec = response.xpath('//div[@id="M_"]')
        # 正文内容获取小心 未必只有一条内容
        content = ''.join(cont_selec.xpath('.//span[@class="ctt"]//text()').extract())
        posted_at = cont_selec.xpath('.//span[@class="ct"]//text()').extract_first(default=None)
        # 之后可能要用到
        user = cont_selec.xpath('.//a//text()').extract_first()
        comment_count = response.xpath('//span[@class="pms"]//text()').re_first('评论\[(.*?)\]')
        forward_count = response.xpath('//a[contains(., "转发[")]//text()').re_first('转发\[(.*?)\]')
        like_count = response.xpath('//a[contains(., "赞[")]//text()').re_first('赞\[(.*?)\]')

        weiboitem = WeiboContItem()
        # 使用动态监测赋值 但是需要小心eval可能有异常
        for field in weiboitem.fields:
            # fields是set类型 存储每个键值集合
            # 访问对象的[key]即调用__getitem__()方法 获得内部value字典存储的数据

            try:
                weiboitem[field] = eval(field)
            except NameError:
                self.logger.error("field is not defined",field)
        yield weiboitem


