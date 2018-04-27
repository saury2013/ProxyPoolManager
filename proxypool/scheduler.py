# -*- coding: utf-8 -*-
__author__ = 'Allen'

import time
from multiprocessing import Process
from proxypool.server import app
from proxypool.importer import Importer
from proxypool.tester import Tester
from proxypool.conf import *

class Scheduler():
    def schedule_tester(self,cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            print('run test...')
            tester.run()
            time.sleep(cycle)

    def schedule_importer(self,cycle=GETTER_CYCLE):
        importer = Importer()
        while True:
            print('importer run...')
            importer.import_from_net()
            time.sleep(cycle)
    def schedule_server(self):
        print('server run in ',SERVER_HOST,':',SERVER_PORT)
        app.run(SERVER_HOST,SERVER_PORT)

    def run(self):
        print('ProxyManager running...')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if IMPORTER_ENABLED:
            importer_process = Process(target=self.schedule_importer)
            importer_process.start()
        if SERVER_ENABLED:
            server_process = Process(target=self.schedule_server)
            server_process.start()