# _*_coding:utf-8 _*_
import pickle
import hashlib

'''
-------------------------------------------------
   @File Name :     URLManager
   @Description :   *
   @Author :        YYP
   @date :          2020/4/20
   @modify :        2020/4/20
-------------------------------------------------
'''

class UrlManager:
    def __init__(self):
        self.new_urls = self.load_progress('new_url.txt')  # 未爬取的URL集合
        self.old_urls = self.load_progress('old_url.txt')  # 已爬取的URL集合

    def has_new_url(self):
        return self.new_url_size() != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        m = hashlib.md5()
        m.update(new_url)
        self.old_urls.add(m.hexdigest()[8: -8])
        return new_url

    def add_new_url(self, url):
        if url is None:
            return
        m = hashlib.md5()
        m.update(url)
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        return len(self.new_urls)

    def old_url_size(self):
        return len(self.old_urls)

    def save_progress(self, path, data):
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def load_progress(selfs, path):
        print("从文件加载进度：%s" % path)
        try:
            with open(path, 'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except:
            print('无进度文件，创建：%s' % path)
        return set()