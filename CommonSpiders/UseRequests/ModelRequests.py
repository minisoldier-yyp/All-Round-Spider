# _*_coding:utf-8 _*_
import requests
from loguru import logger
from requests import ConnectionError, HTTPError, Timeout, TooManyRedirects
from retry import retry


'''
-------------------------------------------------
   @File Name :     model_requests
   @Description :   create requests object
   @Author :        YYP
   @date :          2020/4/21
   @modify :        2020/4/21
-------------------------------------------------
'''

class ModelRequests:
    """
    use requests lib create a Web Request object
    """
    def __init__(self):
        # 初始化会话
        self.sess = requests.Session()

        # 固定值，可设置更改
        self._encoding = 'utf-8'

        self.timeout = 5

        # 多个接收内容，调用可返回
        self.response = None
        self.status_code = ''
        self.headers = ''
        self.content = None
        self.html = ''
        self.json_content = None
        self.cookies = None
        self.flag = False

        # 带传入值
        self.url = ''
        self.data = {}
        self.params = {}


    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, encode):
        self._encoding = encode
        if self.response:
            self.response.encoding = encode

    def set_timeout(self, timeout):
        self.timeout = timeout

    def get_flag(self):
        return self.flag

    @retry(exceptions=Timeout, tries=3)
    def get_response(self, url, **other_params):
        self.flag = False
        params = other_params.get('params', None)
        data = other_params.get('data', None)
        headers = other_params.get('headers', None)
        auth = other_params.get('auth', None)
        timeout = other_params.get('timeout', self.timeout)
        proxies = other_params.get('proxies', None)
        hooks = other_params.get('hooks', None)
        stream = other_params.get('stream', None)
        verify = other_params.get('verify', None)
        cert = other_params.get('cert', None)
        json = other_params.get('json', None)
        try:
            logger.debug("尝试使用 ”GET“ 方法访问网址：[ {web_url} ] ,参数包括 {other_params}", web_url=url, other_params=other_params)
            self.response = self.sess.get(url=url, params=params, data=data, headers=headers, auth=auth, timeout=timeout, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
            logger.debug("成功使用 ”GET“ 方法访问网址：[ {web_url} ] ", web_url=url)
            self.response.encoding = self._encoding
            logger.debug("修改接收编码encoding = {encode}", encode=self._encoding)
            self.flag = True
            self.init()
        except ConnectionError as e:
            logger.error("网址 [{web_url}] DNS查询失败或者拒绝连接，请确认重试！ \n 具体原因为{e}", web_url=url, e=e)
        except HTTPError as e:
            logger.error("网址 [{web_url}] 返回了不正确的状态码，请确认重试！ \n 具体原因为{e}", web_url=url, e=e)
        except TooManyRedirects as e:
            logger.error("网址 [{web_url}] 重定向次数过多，请确认重试！ \n 具体原因为{e}", web_url=url, e=e)

    @retry(exceptions=Timeout, tries=3)
    def post_response(self, url, **other_params):
        self.flag = False
        params = other_params.get('params', None)
        data = other_params.get('data', None)
        headers = other_params.get('headers', None)
        auth = other_params.get('auth', None)
        timeout = other_params.get('auth', self.timeout)
        proxies = other_params.get('proxies', None)
        hooks = other_params.get('hooks', None)
        stream = other_params.get('stream', None)
        verify = other_params.get('verify', None)
        cert = other_params.get('cert', None)
        json = other_params.get('json', None)
        try:
            logger.debug("尝试使用 ”POST“ 方法访问网址：[ {web_url} ] ,参数包括{other_params}", web_url=url, other_params=other_params)
            self.response = self.sess.post(url=url, params=params, data=data, headers=headers, auth=auth, timeout=timeout, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
            logger.debug("成功使用 ”POST“ 方法访问网址：[ {web_url} ] ", web_url=url)
            self.response.encoding = self._encoding
            logger.debug("修改接收编码encoding = {encode}", encode=self._encoding)
            self.flag = False
            self.init()
        except ConnectionError as e:
            logger.error("网址 [{web_url}] DNS查询失败或者拒绝连接，请确认重试！ \n 具体原因为{e}", web_url=url, e=e)
        except HTTPError as e:
            logger.error("网址 [{web_url}] 返回了不正确的状态码，请确认重试！ \n 具体原因为{e}", web_url=url, e=e)
        except TooManyRedirects as e:
            logger.error("网址 [{web_url}] 重定向次数过多，请确认重试！ \n 具体原因为{e}", web_url=url, e=e)


    def init(self):
        logger.debug("使用最新接收更新 [status_code] [headers] [content] [html] [cookies]")
        self.status_code = self.response.status_code
        self.headers = self.response.headers
        self.content = self.response.content
        self.html = self.response.text
        # self.cookies = self.response.cookies()
        if "application/json" in self.headers['content-type']:
            self.json_content = self.response.json()

    def get_html(self):
        return self.html

    def get_content(self):
        return self.content

    def get_json(self):
        return self.json_content
