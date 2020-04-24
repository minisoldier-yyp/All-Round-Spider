# _*_coding:utf-8 _*_
from threading import Thread
from queue import Empty, Queue
from ..Manager.ProxyManager import ProxyManager
from loguru import logger
from ..Proxy.Proxy import Proxy
'''
-------------------------------------------------
   @File Name :     *
   @Description :   *
   @Author :        YYP
   @date :          2020/4/20
   @modify :        2020/4/20
-------------------------------------------------
'''

class UsefulProxyCheck(ProxyManager, Thread):
    def __init__(self, queue, thread_name):
        ProxyManager.__init__(self)
        Thread.__init__(self, name=thread_name)
        self.log = logger
        self.queue = queue

    def run(self):
        self.log.info("RawProxyCheck - {}  : start".format(self.name))
        while True:
            try:
                proxy = self.queue.get(block=False)
            except Empty:
                self.log.info("RawProxyCheck - {}  : exit".format(self.name))
                break
            proxy.check_proxy_useful()
            if proxy.proxy_score != 0:
                self.update_proxy(proxy)
                # if self.db.get(proxy.ip):
                #     self.update_proxy(proxy)
                # else:
                #     self.insert_proxy(proxy)
            else:
                self.delete(proxy.ip)
            self.queue.task_done()


def do_useful_proxy_check():
    proxy_queue = Queue()
    for each_proxy in ProxyManager().get_all():
        proxy_queue.put(each_proxy)

    thread_list = list()
    for index in range(20):
        thread_list.append(UsefulProxyCheck(proxy_queue, "thread_%s" % index))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()
