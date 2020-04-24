# _*_coding:utf-8 _*_
from utils.db_mysql.mysql_client import connect_db
import os
from loguru import logger
from utils import util_functions
from utils.IpPool.Proxy.Proxy import Proxy
import random

'''
-------------------------------------------------
   @File Name :     ProxyManager
   @Description :   create Proxy Manager
   @Author :        YYP
   @date :          2020/4/22
   @modify :        2020/4/22
-------------------------------------------------
'''

def get_basic_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def format_proxy(one_proxy):
    tmp_proxy = Proxy(one_proxy[0], one_proxy[1], proxy_score=int(one_proxy[6]), proxy_agreement=int(one_proxy[2]),
                 proxy_anonymity=int(one_proxy[3]), proxy_source=one_proxy[4], create_time=float(one_proxy[5]), last_vaild_time=float(one_proxy[7]))
    return tmp_proxy

class ProxyManager:
    def __init__(self):
        self.db = connect_db(
            util_functions.cfg_parse(os.path.join(get_basic_path(), 'Config', 'MysqlSettings.cfg'))
        )
        self.table = 'proxyInfo'

    def get(self, proxyIP):
        sql = "select * from ProxyInfo where proxyIP='{}'".format(proxyIP)
        query_proxy = self.db.query(sql, fetchone=True, execute=True)
        if not query_proxy:
            return None
        get_proxy = format_proxy(self.db.query(sql, fetchone=True, execute=True))
        if get_proxy:
            return get_proxy

    def update_proxy(self, proxy):
        ip = proxy._proxy_ip
        data = {
            "proxyPort": proxy.port,
            "proxyScore": proxy.proxy_score,
            "proxyAgreement": proxy._proxy_agreement,
            "proxyAnonymity": proxy._proxy_anonymity,
            "proxyCreateTime": proxy._create_time,
            "proxyLastVaildTime": proxy._last_vaild_time,
            "proxySource": proxy._proxy_source,
        }
        self.db.update(self.table, data=data, condition="proxyIP='{}'".format(ip))

    def insert_proxy(self, proxy):
        data = {
            "proxyIP": proxy._proxy_ip,
            "proxyPort": proxy.port,
            "proxyScore": proxy.proxy_score,
            "proxyAgreement": proxy._proxy_agreement,
            "proxyAnonymity": proxy._proxy_anonymity,
            "proxyCreateTime": proxy._create_time,
            "proxyLastVaildTime": proxy._last_vaild_time,
            "proxySource": proxy._proxy_source,
        }
        self.db.insert(self.table, data)

    def get_one(self):
        item_list = self.db.fetch_rows('ProxyInfo', order='proxyScore')
        if item_list:
            random_choice = random.choice(item_list)
            return format_proxy(random_choice)
        return None

    def delete(self, proxyIP):
        self.db.delete('ProxyInfo', 'proxyIP="{}"'.format(proxyIP))

    def get_all(self):
        proxy_list = []
        for each_proxy in self.db.fetch_rows('ProxyInfo', order='proxyScore'):
            tmp_proxy = [each_proxy['proxyIP'], each_proxy['proxyPort'], each_proxy['proxyAgreement'],
                         each_proxy['proxyAnonymity'], each_proxy['proxySource'], each_proxy['proxyCreateTime'],
                         each_proxy['proxyScore'], each_proxy['proxyLastVaildTime']]
            proxy_list.append(format_proxy(tmp_proxy))
        return proxy_list

    def getNumber(self):
        return self.db.count('ProxyInfo')
