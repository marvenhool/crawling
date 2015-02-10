# This Python file uses the following encoding: utf-8
import crawling_module
import time
#システムのディフォルトコードセットをUTF-８に設定、
#でないとASCIIコード直接ファイルに書き込みできない可能性が高いですから、エラー出る

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from selenium import webdriver
driver = webdriver.Chrome()
driver.maximize_window()

#クロム、そのほかのウェブブラウザを使う場合必ずブラウザドライブをデフォルトパスに保存しておいてください。
#クロムの場合、chormedriver.exeが必要です。

driver.get('http://www.athome.co.jp/est_top/me_20/1_12_13')
#ロード完了までしばらく待つ
time.sleep(5)

driver.execute_script('javascript:Dialog.searchList(13101)')
time.sleep(10)

# #検索結果に１０番目ページに遷移
driver.execute_script('javascript:List.pageList(10)')
time.sleep(10)

#JS実行完了のページソースを取得

#タッグ内の値だけを取得
body_text = driver.find_element_by_tag_name('body').text

#JS実行後のソースを取得
_html = driver.find_element_by_xpath('/html')
html_text = _html.get_attribute('outerHTML')

#エレメントIDでエレメントを取得
checkbox_element = driver.find_element_by_id('MES06')



#別コードセットからUTF-8コードに変更
#html = buf.decode('shift_jis').encode('utf-8')

#   ......data analysis......
#ここは取得したページソースを処理、処理データをファイルに書き込み

#取得した内容をファイルに書き込み
crawling_module.write_text_to_file_by_utf8('body.csv', body_text)
crawling_module.write_text_to_file_by_utf8('html.csv', html_text)

# #必ず使用完了のIEオブジェクトを解放
driver.quit()

