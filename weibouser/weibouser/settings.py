# -*- coding: utf-8 -*-

# Scrapy settings for weibouser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weibouser'

SPIDER_MODULES = ['weibouser.spiders']
NEWSPIDER_MODULE = 'weibouser.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weibouser (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'accept':' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding':' gzip, deflate, br',
    'accept-language':' zh-CN,zh;q=0.9',
    'cache-control':' max-age=0',
    'cookie':'_T_WM=48950117954; ALF=1560173355; SCF=AkdNqmbFG1ZxtQbKRVV2eFK9U0vpgsuoC-SP4_hXtyQ-H_V_yVWSfu99l3DC0gFVLeUM6yQM24oj5Wu2SJGoeeI.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh6BG_pevVvPXfx08sbfjTg5JpX5KzhUgL.FoqXehzN1K.fSKn2dJLoI0Uui--Xi-iWi-iWi--NiKLWiKnXi--fiK.7iKy2i--ci-27iK.pi--NiKLWiKnXi--fi-i2i-zp; SUB=_2A25x57vMDeRhGeBK61AW-SfJzjSIHXVTK8WErDV6PUJbkdAKLXf6kW1NR-XwGCmVgo7YLVz7f_h0O0gM0GUo9ZCD; SUHB=0G0uBK6WbzhZbg; SSOLoginState=1558432668',
    'upgrade-insecure-requests':' 1',
    'user-agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # 'weibouser.middlewares.WeibouserSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
# middleware 需要添加在downloadmoddleware部分才有效
#    'weibouser.middlewares.CookiesMiddleware': 543,
    'weibouser.middlewares.WeibouserDownloaderMiddleware': 543,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'weibouser.pipelines.WeibouserPipeline': 300,
   'weibouser.pipelines.MongoPipline':301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

COOKIESPOOL_URL = 'http://localhost:5000/weibo/random'

MONGO_URI = 'localhost'
MONGO_DB = 'weibo'