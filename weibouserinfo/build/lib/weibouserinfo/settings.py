# -*- coding: utf-8 -*-

# Scrapy settings for mweibouser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html



SPIDER_MODULES = ['weibouserinfo.spiders']
NEWSPIDER_MODULE = 'weibouserinfo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mweibouser (+http://www.yourdomain.com)'

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
    'accept':' application/json, text/plain, */*',
    'accept-encoding':' gzip, deflate, br',
    'accept-language':' zh-CN,zh;q=0.9',
    'cookie':' _T_WM=52231965963; SUB=_2A25x4SwTDeRhGeBK61AW-SfJzjSIHXVTLbRbrDV6PUJbkdAKLVnhkW1NR-XwGFRISiLY2EfW5-QKms6sVZdTvrsN; SUHB=0BLo0YkHGQ8ACj; SCF=Atd-xXDCx7-dmiWylV3LoyUwdqvJWJr78FXmI18qlMhqonzre1Fw3W5iq64DqA8t1RkTcNudoO7uIJ_MYA4PQgg.; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=49da94; M_WEIBOCN_PARAMS=fid%3D2304132405925587_-_WEIBO_SECOND_PROFILE_WEIBO%26uicode%3D10000011',
    'user-agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'x-requested-with':' XMLHttpRequest',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'mweibouser.middlewares.MweibouserSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 启用middleware为了有效 需要优先于默认的cookie以及proxy代理
    # ？？？
    # 'mweibouser.middlewares.CookiesMiddleWare' : 553,
    # 'mweibouser.middlewares.ProxiesMiddleWare' : 555
}
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
    'weibouserinfo.pipelines.FormatTimePipeLine':300,
    'weibouserinfo.pipelines.TimePipeLine': 301,
    # 存储管道需要最后经过
    'weibouserinfo.pipelines.MongoPipeLine': 302,
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

# 设置数据库连接信息
# MONGO_URI = 'localhost'
# MONGO_DB = 'mweibo_info'

# 是指cookies api获取接口
COOKIES_URL = 'http://localhost:5000/weibo/random'
PROXY_URL = 'http://localhost:5555/random'

# mongodb 链接信息

MONGO_DB = 'mweibo_info'

# 分布式部署
MONGO_URI = '152.136.125.90'
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_URL = 'redis://:123456@152.136.125.90:6379'
# ？？
# 作为封ip的标志 从而使用代理 会自动在request中判断
# 并且自动在retry_times字段中赋值 不需要人为操作
RETRY_HTTP_CODES = [401, 403, 408, 414, 500, 502, 503, 504]


# curl http://192.168.233.66:6800/schedule.json -d project=mweibouser -d spider=mwbspider
# curl http://192.168.233.66:6800/cancel.json -d project=mweibouser -d job=

# curl http://152.136.125.90:6800/schedule.json -d project=mweibouser -d spider=mwbspider
# curl http://152.136.125.90:6800/cancel.json -d project=mweibouser -d job=