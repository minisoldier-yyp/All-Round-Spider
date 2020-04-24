# _*_coding:utf-8 _*_
import requests
from loguru import logger
import configparser
'''
-------------------------------------------------
   @File Name :     util_functions
   @Description :   put util function
   @Author :        YYP
   @date :          2020/4/21
   @modify :        2020/4/21
-------------------------------------------------
'''

def valid_proxy_useful(proxy):
    """
    检查代理可用性
    :param proxy: 代理
    :return: 代理分数
    """
    time_out_list = [3, 5, 7]
    proxy_score = 0
    for each_time_out in time_out_list:
        try:
            r = requests.get('http://www.baidu.com', proxies=proxy, timeout=each_time_out, verify=False)
            if r.status_code == 200:
                if each_time_out == 3:
                    proxy_score += 50
                elif each_time_out == 5:
                    proxy_score += 30
                elif each_time_out == 7:
                    proxy_score += 20
        except Exception as e:
            pass
    return proxy_score

def cfg_parse(file_path):
    cf = configparser.ConfigParser()
    cf.read(file_path)
    return cf
