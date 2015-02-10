# This Python file uses the following encoding: utf-8
import crawling_module
import time
#システムのディフォルトコードセットをUTF-８に設定、
#でないとASCIIコード直接ファイルに書き込みできない可能性が高いですから、エラー出る

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib
import time
import os
from selenium import webdriver

class Crawler:

    def __init__(self):
        self.url = 'http://tabelog.com/tokyo/A1307/A130701/13000002/'
        self.img_xpath = '//ul/li/div/a/img'
        self.img_url_dic = {}

    def launch(self):
        #driver = webdriver.Chrome()
        #driver.maximize_window()
        #driver.get(self.url)
        filepath = os.getcwd()
        urllib.urlretrieve('http://image1-2.tabelog.k-img.com/restaurant/images/Rvw/30472/640x640_rect_30472480.jpg', filepath + '\images\sina.jpg')
        time.sleep(1)

if __name__ == '__main__':
    crawler = Crawler()
    crawler.launch()