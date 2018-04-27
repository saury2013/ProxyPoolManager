# -*- coding: utf-8 -*-
__author__ = 'Allen'

from proxypool.db_connector import RedisClient
from proxypool.excavator import Crawler
from proxypool.conf import *
import sys

class Importer():

    def __init__(self):
        self.redis_client = RedisClient()
        self.crawler = Crawler()

    def is_over_shreshold(self):
        #判断代理池是否已经到达限制
        if self.redis_client.get_count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    def import_from_net(self):
        print('import proxy from internet...')
        if not self.is_over_shreshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                sys.stdout.flush()
                if proxies:
                    for proxy in proxies:
                        self.redis_client.add(proxy)
    def import_by_hand(self):
        print('Please input proxy,enter exit for quit...')
        while True:
            proxy = input()
            if proxy == 'exit':
                break
            result = self.redis_client.add(proxy)
            print('success' if result else 'failed')


if __name__ == '__main__':
    importer = Importer()
    importer.import_from_net()
