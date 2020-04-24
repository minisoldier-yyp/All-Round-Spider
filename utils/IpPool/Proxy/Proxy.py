# _*_coding:utf-8 _*_
from utils.util_functions import valid_proxy_useful
import time

'''
-------------------------------------------------
   @File Name :     Proxy.py
   @Description :   每个IP代理的基础类
   @Author :        YYP
   @date :          2020/4/20
   @modify :        2020/4/20
-------------------------------------------------
'''

class Proxy:
    """
    代理基础类
    """
    def __init__(self, proxy_ip, proxy_port, proxy_score=0, proxy_agreement=2,
                 proxy_anonymity=2, proxy_source='', create_time="", last_vaild_time=""):
        """
        :param proxy_ip:        代理IP
        :param proxy_port:      端口号
        :param proxy_score:     该代理的分数，可以判断该IP是否可用
        :param proxy_agreement: 代理协议，分为了三种 http https 和 http,https
        :param proxy_anonymity: 代理匿名程度：透明 匿名 高匿
        :param proxy_source:    代理来源：西刺 快代理等
        :param create_time:     创建时间： 从网页上获取时的时间
        :param last_vaild_time: 最后验证时间
        """
        self._proxy_ip = proxy_ip
        self._proxy_port = proxy_port
        self._proxy_score = proxy_score
        self._proxy_agreement = proxy_agreement
        self._proxy_anonymity = proxy_anonymity
        self._create_time = create_time
        self._last_vaild_time = last_vaild_time
        self._proxy_source = proxy_source

    @property
    def ip(self):
        return self._proxy_ip

    @property
    def port(self):
        return self._proxy_port

    @property
    def proxy(self):
        if not isinstance(self._proxy_agreement, int):
            return None
        if self._proxy_agreement == 0:
            return {'http': 'http://' + self._proxy_ip + ':' + str(self._proxy_port)}
        elif self._proxy_agreement == 1:
            return {'https': 'https://'+self._proxy_ip + ':' + str(self._proxy_port)}
        else:
            return {
                'http': 'http://' + self._proxy_ip + ':' + str(self._proxy_port),
                'https': 'https://' + self._proxy_ip + ':' + str(self._proxy_port)
            }

    @property
    def proxy_score(self):
        return self._proxy_score

    @proxy_score.setter
    def proxy_score(self, score):
        assert isinstance(score, int), '赋值失败，请赋值正确的Score，整数类型（int）'
        self._proxy_score = score

    @property
    def proxy_agreement(self):
        if not isinstance(self._proxy_agreement, int):
            return None
        if self._proxy_agreement == 0:
            return 'http'
        elif self._proxy_agreement == 1:
            return 'https'
        else:
            return 'http,https'

    @property
    def proxy_anonymity(self):
        if not isinstance(self._proxy_anonymity, int):
            return None
        if self._proxy_anonymity == 0:
            return '透明代理'
        elif self._proxy_agreement == 1:
            return '匿名代理'
        else:
            return '高匿代理'

    @property
    def create_time(self):
        if not isinstance(self._create_time, float):
            return None
        create_time_array = time.localtime(self._create_time)
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", create_time_array)
        return create_time

    @property
    def last_vaild_time(self):
        if not isinstance(self._last_vaild_time, float):
            return None
        last_vaild_time_array = time.localtime(self._last_vaild_time)
        last_vaild_time = time.strftime("%Y-%m-%d %H:%M:%S", last_vaild_time_array)
        return last_vaild_time

    @last_vaild_time.setter
    def last_vaild_time(self, last_vaild_time):
        assert isinstance(last_vaild_time, float), '赋值失败，请赋值时间戳，为浮点类型（float）'
        self._last_vaild_time = last_vaild_time

    @property
    def proxy_source(self):
        return self._proxy_source

    @property
    def info_dict(self):
        """ 属性字典 """
        return {"proxy": self.proxy,
                "proxy_score": self.proxy_score,
                "proxy_agreement": self.proxy_agreement,
                "proxy_anonymity": self.proxy_anonymity,
                "create_time": self.create_time,
                "last_vaild_time": self.last_vaild_time,
                "proxy_source": self.proxy_source}

    @property
    def is_useful(self):
        if not isinstance(self.proxy_score, int):
            return None
        if self.proxy_score == 0:
            return False
        else:
            return True

    def check_proxy_useful(self):
        """检测代理是否可用"""
        proxy_score = valid_proxy_useful(self.proxy)
        self.proxy_score = proxy_score
        self.last_vaild_time = time.time()
