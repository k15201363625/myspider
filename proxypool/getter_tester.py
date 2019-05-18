import aiohttp
import asyncio
import sys
import time
from aiohttp import ClientError

from proxypool.settings import *
from proxypool.database import RedisClient
from proxypool.crawers import Crawler

class Tester:
    '''
    由于测试代理基本就是访问 访问时间成为程序瓶颈
    所以借助aiohttp进行异步访问
    '''
    # 注意aiohttp，async的书写格式：session get 都需要使用async声明
    def __init__(self):
        self.redis = RedisClient()

    async def testOne(self,proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False) #??
        try:
            async with aiohttp.ClientSession(connector=conn) as sess:
                if isinstance(proxy, bytes): #??
                    proxy = proxy.decode('utf-8')
                new_proxy = 'http://'+proxy
                print('testing proxy is:',new_proxy)
                async with sess.get(TEST_URL,proxy=new_proxy,timeout=10,allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        # 跳转码 200都认为成功
                        self.redis.setmax(proxy)
                        print(proxy,' is useful')
                    else:
                        self.redis.decrease(proxy)
                        print(proxy,' is non-available')
        except (ClientError,ConnectionError,asyncio.TimeoutError):
            # concurrent.futures._base.TimeoutError 基本都是超时导致的错误
            self.redis.decrease(proxy)
            # print(e)
            print('error in test proxy')


    def __async_opt(self,proxies):
        loop = asyncio.get_event_loop()
        tasks = [self.testOne(proxy) for proxy in proxies]
        # 必须小心 坑 为了发挥异步作用 需要为tasks生成等待队列
        loop.run_until_complete(asyncio.wait(tasks))


    def run_tester(self):
        print('testing start')
        count = self.redis.count()
        print('all proxy count is:',count)
        for i in range(0,count,BATCH_TEST_SIZE):
            cur_start = i
            cur_stop = min(i+BATCH_TEST_SIZE,count)
            cur_proxies = self.redis.getbatch(cur_start,cur_stop)
            print('testing from',cur_start+1,'--',cur_stop)
            self.__async_opt(cur_proxies)
            sys.stdout.flush()
            time.sleep(BATCH_TEST_WAIT_TIME)



class Getter:
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def run_getter(self):
        print('getting start')
        if self.redis.count() <= POOL_UPPER_THRESHOLD:
            # 调用clawer方法
            for callfunc in self.crawler.__crawlfuncs__:
                proxies = self.crawler.get_proxies(callfunc)
                sys.stdout.flush()
                for proxy in proxies:
                    self.redis.add(proxy)
        else:
            print('now pool is over thershold')

