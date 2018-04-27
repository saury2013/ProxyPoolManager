# -*- coding: utf-8 -*-
__author__ = 'Allen'

import asyncio
import aiohttp
import time
import sys
try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.db_connector import RedisClient
from proxypool.conf import *

class Tester(object):
    def __init__(self):
        self.redis_client = RedisClient()

    async def test_single_proxy(self,proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('test proxy:',proxy)
                async with session.get(TEST_URL,proxy=real_proxy,timeout=15,allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis_client.set_max(proxy)
                        print('validate proxy:',proxy)
                    else:
                        self.redis_client.decrease(proxy)
                        print('request status code illegal->',response.status,'[proxy]:',proxy)
            except (ClientError,aiohttp.client_exceptions.ClientConnectionError,asyncio.TimeoutError,AttributeError):
                self.redis_client.decrease(proxy)
                print('bad proxy:',proxy)

    def run(self):
        try:
            count = self.redis_client.get_count()
            print('There are ',count,' proxy in proxypool.')
            for i in range(0,count,BATCH_TEST_SIZE):
                start = i
                stop = min(i+BATCH_TEST_SIZE,count)
                print('Testing proxy:',start+1,'--',stop)
                test_proxies = self.redis_client.batch(start,stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('Tester catch a error:',e.args)
