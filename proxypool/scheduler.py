import sys
import io
import time
from multiprocessing import Process
from proxypool.getter_tester import Getter,Tester
from proxypool.flaskapi import app
from proxypool.settings import *

# 为了减少输出消耗 使用buffer包装 生成带有buffer的文本输出流
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') 一运行就卡主
'''
使用多进程进行调度
根据setting中的开关进行调度
'''

class Scheduler:
    def schedule_tester(self,cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            print('new cycle test start')
            tester.run_tester()
            time.sleep(cycle)
    def schedule_getter(self,cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            print('new cycle get start')
            getter.run_getter()
            time.sleep(cycle)
    def schedule_api(self):
        app.run(API_HOST,API_PORT)

    def scheduler_run(self):
        print('proxy pool start')
        # 生成相应的进程 并且开始运行
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

if __name__ == '__main__':
    test = Scheduler()
    # test.schedule_getter()
    test.schedule_tester()
    # test.schedule_api()
