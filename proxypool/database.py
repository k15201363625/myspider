import re
import redis
from random import choice
# 外面不能嵌套文件夹 否则pycharm检测不到import
from proxypool.settings import *
from proxypool.proxypoolerror import PoolEmptyError

# based sorted set
# 可以根据指定的关键字进行排序
class RedisClient:
    def __init__(self,host=REDIS_HOST,password=REDIS_PASSWORD,port=REDIS_PORT):
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)
        if self.db != None:
            print('connection successfully')

    def add(self,proxy,score=INITIAL_SCORE):
        # 不重复才添加 检查格式
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+',proxy):
            print('proxy form error',proxy)
            return None
        if not self.db.zscore(REDIS_KEY,proxy):
            # 添加 score-name pair
            return self.db.zadd(REDIS_KEY,score,proxy)
    def decrease(self,proxy):
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score > MIN_SCORE:
            print(proxy,'now score:',score,'-1')
            return self.db.zincrby(REDIS_KEY,proxy,-1)
        else:
            print('proxy:',proxy,' is lost from pool')
            return self.db.zrem(REDIS_KEY,proxy)

    def exists(self,proxy):
        return self.db.zscore(REDIS_KEY,proxy) != None

    def setmax(self,proxy):
        # set 如果有 自动更新score
        print(proxy, 'now score:', MAX_SCORE)
        return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)

    def count(self):
        return self.db.zcard(REDIS_KEY)

    def getall(self):
        # return proxy sorted list
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)

    def getbatch(self,start,stop):
        # return proxy from start to stop - 1 in rev order
        # 不能用zrevrangebyscore
        return self.db.zrevrange(REDIS_KEY,start,stop-1)

    def random(self):
        # 先选择最高分数的
        results = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(results) != 0:
            return choice(results)
        # 随机选择
        else:
            results = self.db.zrevrange(REDIS_KEY,MIN_SCORE,MAX_SCORE)
            if len(results):
                return choice(results)
            else:
                raise PoolEmptyError

if __name__=='__main__':
    conn = RedisClient()
    result = conn.getbatch(1,11)
    print(result)