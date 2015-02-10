# This Python file uses the following encoding: utf-8
import crawling_module
import time
#システムのディフォルトコードセットをUTF-８に設定、
#でないとASCIIコード直接ファイルに書き込みできない可能性が高いですから、エラー出る
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from selenium import webdriver
import selenium.webdriver.chrome.service as service

service = service.Service('/path/to/chromedriver')
service.start()
capabilities = {'chrome.binary': '/path/to/custom/chrome'}
browser = webdriver.Remote(service.service_url, capabilities)
browser.get('http://www.athome.co.jp/est_top/me_20/1_12_13');



import time

from selenium import webdriver
import selenium.webdriver.chrome.service as service

service = service.Service('/path/to/chromedriver')
service.start()
capabilities = {'chrome.binary': '/path/to/custom/chrome'}
driver = webdriver.Remote(service.service_url, capabilities)
driver.get('http://www.google.com/xhtml');
time.sleep(5) # Let the user actually see something!
driver.quit()



#ロード完了までしばらく待つ
time.sleep(5)

browser.execute_script('javascript:Dialog.searchList(13101)')
time.sleep(10)

#検索結果に１０番目ページに遷移
browser.execute_script('javascript:List.pageList(10)')
time.sleep(10)


#JS実行完了のページソースを取得

webElement = browser.find_elements_by_xpath('/html')
buf = webElement.getAttribute('outerHTML')


#別コードセットからUTF-8コードに変更
#html = buf.decode('shift_jis').encode('utf-8')

#   ......data analysis......
#ここは取得したページソースを処理、処理データをファイルに書き込み

#取得した内容をファイルに書き込み
crawling_module.write_text_to_file_by_utf8('buf.csv', buf)

#必ず使用完了のIEオブジェクトを解放
browser.close()

