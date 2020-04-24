# _*_coding:utf-8 _*_
from threading import Thread
from queue import Empty, Queue
from ..Manager.ProxyManager import ProxyManager
from loguru import logger
from ..ProxyFetch.FreeProxyFetcher import GetFreeProxy

'''
-------------------------------------------------
   @File Name :     *
   @Description :   *
   @Author :        YYP
   @date :          2020/4/20
   @modify :        2020/4/20
-------------------------------------------------
'''

class RawProxyCheck(ProxyManager, Thread):
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
            self.log.info("thread {} is check proxy useful".format(self.name))
            proxy.check_proxy_useful()
            if proxy.proxy_score != 0:
                if self.get(proxy.ip):
                    self.update_proxy(proxy)
                else:
                    self.log.info("thread {} is inserting proxy".format(self.name))
                    self.insert_proxy(proxy)
            else:
                pass
            self.queue.task_done()


def do_raw_proxy_check():
    proxy_queue = Queue()
    proxy_get_object = GetFreeProxy()
    logger.info("ProxyFetch: Start")
    proxy_get_object.main()
    logger.info("ProxyFetch: End")
    for each_proxy in proxy_get_object.proxy_list:
        proxy_queue.put(each_proxy)

    thread_list = list()
    for index in range(20):
        thread_list.append(RawProxyCheck(proxy_queue, "thread_%s" % index))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()