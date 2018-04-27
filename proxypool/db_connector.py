# -*- coding: utf-8 -*-
__author__ = 'Allen'

from proxypool.conf import *
import redis
import re
from random import choice
from proxypool.error import ProxyPoolEmptyError

class RedisClient(object):
    def __init__(self,host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)

    def add(self,proxy,score=INITIAL_SCORE):
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+',proxy):
            print('A proxy that does not conform to the specification.',proxy)
            return
        if not self.db.zscore(REDIS_KEY,proxy):
            return self.db.zadd(REDIS_KEY,score,proxy)

    def random(self):
        #随机获取代理，规则：先尝试获取最高分数的代理，不存在则按排名，没有则触发异常
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            raise ProxyPoolEmptyError

    def decrease(self,proxy):
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score > MIN_SCORE:
            print('proxy:',proxy,'**current score:',score,'-1')
            return self.db.zincrby(REDIS_KEY,proxy,-1)
        else:
            print('proxy:',proxy,'**current score:',score,'->remove')
            return self.db.zrem(REDIS_KEY,proxy)

    def exist(self,proxy):
        return not self.db.zscore(REDIS_KEY,proxy) == None

    def set_max(self,proxy):
        #将一个代理的分数设为最高
        return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)
    def get_count(self):
        #获取代理池中代理的总数量
        return self.db.zcard(REDIS_KEY)
    def get_all(self):
        #获取所有代理
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)
    def batch(self,start,stop):
        #批量获取代理
        return self.db.zrevrange(REDIS_KEY,start,stop-1)


if __name__ == '__main__':
    rdb = RedisClient()
    result = rdb.batch(1,10)
    print(len(result))
    print(rdb.get_count())