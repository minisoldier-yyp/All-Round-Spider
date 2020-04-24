# _*_coding:utf-8 _*_
from utils.util_functions import *
import unittest
'''
-------------------------------------------------
   @File Name :     util_functions_test
   @Description :   创建util_function的单元测试
   @Author :        YYP
   @date :          2020/4/20
   @modify :        2020/4/20
-------------------------------------------------
'''

class UtilsFunctionsTest(unittest.TestCase):
    def setUp(self) -> None:
        pass


    def tearDown(self) -> None:
        pass

    def test_cfg_parse(self):
        cfg_file = r'test_data/ProxyGetter.cfg'
        ret = cfg_parse(cfg_file).get('proxygetfunction', 'proxygetter')
        self.assertEqual(ret, 'wuyouFree,liuliuFree,xiciFree,kuaiFree')

if __name__ == "__main__":
    unittest.main()
    # suite = unittest.TestCase()
    # suite.addTest(UtilsFunctionsTest('cfg_parse_test'))
    #
    #
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
