# This Python file uses the following encoding: utf-8
import crawling_module
import PAM30
import time
#システムのディフォルトコードセットをUTF-８に設定、
#でないとASCIIコード直接ファイルに書き込みできない可能性が高いですから、エラー出る
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#IEオブジェクトを構築
ie = PAM30.PAMIE()

#URLをアクセス
ie.navigate('http://www.athome.co.jp/est_top/me_20/1_12_13')
#ロード完了までしばらく待つ
time.sleep(5)

#下記コードがIEオブジェクトを駆使してJS関数を実行
ie.executeJavaScript('javascript:Dialog.searchList(13101)')
time.sleep(10)

#検索結果に１０番目ページに遷移
ie.executeJavaScript('javascript:List.pageList(10)')
time.sleep(10)

#JS実行完了のページソースを取得
buf = ie.outerHTML()

#別コードセットからUTF-8コードに変更
#html = buf.decode('shift_jis').encode('utf-8')

#   ......data analysis......
#ここは取得したページソースを処理、処理データをファイルに書き込み

#取得した内容をファイルに書き込み
crawling_module.write_text_to_file_by_utf8('buf.csv', buf)

#必ず使用完了のIEオブジェクトを解放
ie.quit()

#---------------------------------------------------------------------------------------------