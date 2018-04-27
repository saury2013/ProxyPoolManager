# -*- coding: utf-8 -*-
__author__ = 'Allen'

class ProxyPoolEmptyError(Exception):
    def __init__(self):
        Exception.__init__()

    def __str__(self):
        return repr('ProxyPool have dried up')