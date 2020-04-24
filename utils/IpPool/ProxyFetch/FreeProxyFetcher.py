# _*_coding:utf-8 _*_
import requests
from lxml import etree
import re
import time
from loguru import logger
from CommonSpiders.UseRequests.ModelRequests import ModelRequests
from ..Proxy.Proxy import Proxy
from utils import ua_pool
requests.packages.urllib3.disable_warnings()

'''
-------------------------------------------------
   @File Name :     FreeProxyFetcher.py
   @Description :   Get all free proxy from  "无忧代理" "西刺代理" "快代理" ...
   @Author :        YYP
   @date :          2020/4/21
   @modify :        2020/4/21
-------------------------------------------------
'''

class GetFreeProxy:
    def __init__(self):
        self.res = ModelRequests()
        self._proxy_list = []
        self.logger = logger

    @property
    def proxy_list(self):
        return self._proxy_list

    def wuyouFree(self):
        """
        无忧代理首页20个免费IP  http://www.data5u.com/
        :return: list ip info
        """
        self.logger.debug('正在从无忧代理获取免费IP...')
        url_list = [
            "http://www.data5u.com/",
        ]
        key = 'ABCDEFGHIZ'
        for url in url_list:
            self.res.get_response(url, headers={"User-Agent": ua_pool.get_ua()})
            html_tree = etree.HTML(self.res.get_html())
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                proxyIP = ul.xpath('./span[1]/li/text()')[0]
                port_class = ul.xpath('./span[2]/li/@class')[0].split(' ')[1]
                if ul.xpath('./span[4]/li/text()')[0].lower() == 'http':
                    proxyAgreement = 0
                elif ul.xpath('./span[4]/li/text()')[0].lower() == 'https':
                    proxyAgreement = 1
                else:
                    proxyAgreement = 2
                port_sum = 0
                for p in port_class:
                    port_sum *= 10
                    port_sum += key.index(p)
                proxyPort = port_sum >> 3
                if ul.xpath('./span[3]/li/text()')[0].strip() == '透明':
                    proxyAnonymity = 0
                elif ul.xpath('./span[3]/li/text()')[0].strip() == '匿名':
                    proxyAnonymity = 1
                elif ul.xpath('./span[3]/li/text()')[0].strip() == '高匿':
                    proxyAnonymity = 2
                else:
                    proxyAnonymity = 0
                tmp_proxy = Proxy(proxyIP, proxyPort, proxy_agreement=proxyAgreement,
                                  proxy_anonymity=proxyAnonymity, proxy_source='无忧代理', create_time=time.time())
                self._proxy_list.append(tmp_proxy)

    def liuliuFree(self, getnum=50, anonymoustype='高级匿名', area='国内', proxytype='http,https'):
        """
        66免费高匿IP获取
        几乎没有可用的IP
        :param getnum: 需要提取的IP数量
        :param anonymoustype: 选择匿名级别
        :param area: 选择地区
        :param proxytype: 选择代理类型 http https
        """
        anonymoustype = ['不限匿名性', '透明代理', '普通匿名', '高级匿名', '超级匿名'].index(anonymoustype)
        if anonymoustype == 0 or anonymoustype == 1:
            proxy_anonymity = 0
        elif anonymoustype == 2:
            proxy_anonymity = 1
        elif anonymoustype == 3 or anonymoustype == 4:
            proxy_anonymity = 2
        area = ['国内外', '国内', '国外'].index(area)
        proxytype = ['http', 'https', 'http,https'].index(proxytype)
        start_url = 'http://www.66ip.cn/nm.html'
        fetch_url = 'http://www.66ip.cn/nmtq.php?getnum={getnum}&isp=0&anonymoustype={anonymoustype}&start=&ports=&export=&ipaddress=&area={area}&proxytype={proxytype}&api=66ip'.format(getnum=getnum, anonymoustype=anonymoustype, area=area, proxytype=proxytype)
        headers = {"User-Agent": ua_pool.get_ua()}
        self.res.get_response(start_url, headers=headers)
        self.res.get_response(fetch_url, headers=headers)
        html = self.res.get_html()
        proxy_list = re.findall(r'\n.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})<br />', html, re.S)
        for proxy in proxy_list:
            tmp_proxy = Proxy(proxy[0], proxy[1], proxy_agreement=proxytype,
                                  proxy_anonymity=proxy_anonymity, proxy_source='66代理', create_time=time.time())
            self._proxy_list.append(tmp_proxy)


    def xiciFree(self, page=1):
        """
        从西刺代理网获取代理IP
        :param page: 获取的页数，西刺有很多页
        :return:
        """
        url = "https://www.xicidaili.com/nn/"
        headers = {"User-Agent": ua_pool.get_ua()}
        for page_num in range(1, page+1):
            self.res.get_response(url=url+str(page_num), headers=headers)
            html = self.res.get_html()
            html_tree = etree.HTML(html)
            proxy_list = html_tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
            for proxy in proxy_list:
                proxyIP = proxy.xpath('./td')[1].text
                proxyPort = proxy.xpath('./td')[2].text
                if proxy.xpath('./td')[5].text.lower() == 'http':
                    proxyAgreement = 0
                elif proxy.xpath('./td')[5].text.lower() == 'https':
                    proxyAgreement = 1
                else:
                    proxyAgreement = 2
                proxyAnonymity = proxy.xpath('./td')[4].text
                tmp_proxy = Proxy(proxyIP, proxyPort, proxy_agreement=proxyAgreement,
                                  proxy_anonymity=2, proxy_source='西刺代理', create_time=time.time())
                self._proxy_list.append(tmp_proxy)

    def kuaiFree(self, page=1):
        url = 'https://www.kuaidaili.com/free/inha/{}/'
        headers = {"User-Agent": ua_pool.get_ua()}
        for page_num in range(1, page+1):
            self.res.get_response(url=url.format(page_num), headers=headers)
            html = self.res.get_html()
            html_tree = etree.HTML(html)
            proxy_list = html_tree.xpath('.//table/tbody/tr')
            for proxy in proxy_list:
                proxyIP = proxy.xpath('./td')[0].text
                proxyPort = proxy.xpath('./td')[1].text
                if proxy.xpath('./td')[3].text.lower() == 'http':
                    proxyAgreement = 0
                elif proxy.xpath('./td')[3].text.lower() == 'https':
                    proxyAgreement = 1
                else:
                    proxyAgreement = 2
                proxyAnonymity = 2 if proxy.xpath('./td')[2].text[:2] == '高匿' else 0
                tmp_proxy = Proxy(proxyIP, proxyPort, proxy_agreement=proxyAgreement,
                                  proxy_anonymity=proxyAnonymity, proxy_source='快代理', create_time=time.time())
                self._proxy_list.append(tmp_proxy)

    def main(self):
        self.wuyouFree()
        self.liuliuFree()
        self.xiciFree()
        self.kuaiFree()