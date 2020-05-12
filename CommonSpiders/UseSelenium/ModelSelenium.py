# _*_coding:utf-8 _*_
from selenium import webdriver

'''
-------------------------------------------------
   @File Name :     *
   @Description :   *
   @Author :        YYP
   @date :          2020/4/20
   @modify :        2020/4/20
-------------------------------------------------
'''

class SeleniumModel:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)  # excutable_path="webdriver路径"
        self.html = None
        self.handles = {}


    def get_response(self, url, url_id='_default_'):
        self.browser.get(url)
        self.html = self.browser.page_source
        self.handles[url_id] = self.browser.window_handles[-1]

    def switch_window(self, url_id):
        self.browser.switch_to.window(self.handles[url_id])

    def exec_script(self, script):
        self.browser.execute_script(script)  # window.scrollTo(0, document.body.scrollHeight)

    def get_text(self, str_content):
        """
        在源码中查找是否有指定字符串
        :param str_content: 指定的字符串
        :return: 如果没有找到则返回-1
        """
        return self.browser.page_source.find(str_content)

    def get_one_by_xpath(self, xpath):
        return self.browser.find_element_by_xpath(xpath)

    def get_muti_by_xpath(self, xpath):
        return self.browser.find_elements_by_xpath(xpath)

    def get_by_id(self, id):
        return self.browser.find_element_by_id(id)

    def get_one_by_class_name(self, class_name):
        return self.browser.find_element_by_class_name(class_name)

    def get_muti_by_class_name(self, class_name):
        return self.browser.find_elements_by_class_name(class_name)

    def get_muti_by_css(self, css):
        return self.browser.find_elements_by_css_selector(css)

    def get_one_by_css(self, css):
        return self.browser.find_element_by_css_selector(css)

    def get_one_by_tag_name(self, tag_name):
        return self.browser.find_element_by_tag_name(tag_name)

    def get_muti_by_tag_name(self, tag_name):
        return self.browser.find_elements_by_tag_name(tag_name)

    def get_one_by_name(self, name):
        return self.browser.find_element_by_name(name)

    def get_muti_by_name(self, name):
        return self.browser.find_elements_by_name(name)

    def exit(self):
        self.browser.quit()
