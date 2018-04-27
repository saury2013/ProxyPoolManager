# -*- coding: utf-8 -*-
__author__ = 'Allen'

import requests
from requests.exceptions import ConnectionError


base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

def get_page(url,options={}):
    #解析代理网站
    headers = dict(base_headers,**options)
    print('parse website:',url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print('connet failed:',url)
            return None
    except ConnectionError:
        print('connet failed:',url)
        return None