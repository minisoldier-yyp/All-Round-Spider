# _*_coding:utf-8 _*_
from apscheduler.schedulers.blocking import BlockingScheduler
from utils.IpPool.ProxyScheduler.RowProxyCheck import do_raw_proxy_check
from utils.IpPool.ProxyScheduler.UsefulProxyCheck import do_useful_proxy_check
from loguru import logger
'''
-------------------------------------------------
   @File Name :     scheduler_main
   @Description :   Fixed time refresh ip pool
   @Author :        YYP
   @date :          2020/4/22
   @modify :        2020/4/22
-------------------------------------------------
'''


def raw_proxy_scheduler():
    logger.debug('开始获取各个网站的代理IP...')
    do_raw_proxy_check()


def useful_proxy_scheduler():
    do_useful_proxy_check()


def runScheduler():
    raw_proxy_scheduler()
    useful_proxy_scheduler()

    scheduler_log = logger.add("scheduler_log")
    scheduler = BlockingScheduler()

    scheduler.add_job(raw_proxy_scheduler, 'interval', minutes=30, id="raw_proxy_check", name="raw_proxy定时采集")
    scheduler.add_job(useful_proxy_scheduler, 'interval', minutes=5, id="useful_proxy_check", name="useful_proxy定时检查")

    scheduler.start()


if __name__ == '__main__':
    runScheduler()