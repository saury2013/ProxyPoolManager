# -*- coding: utf-8 -*-
__author__ = 'Allen'

from proxypool.scheduler import Scheduler
import sys,io

#程序入口
sys.stdout  = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def main():
    try:
        scheduler = Scheduler()
        scheduler.run()
    except Exception:
        print('proxypool error')
        # main()

if __name__ == '__main__':
    main()