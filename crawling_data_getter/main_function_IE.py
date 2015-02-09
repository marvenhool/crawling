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

#IEクラスが使える方法

# ステータス　コントロール

# _wait()  : 画面のロード完成を待つ
# _frameWait() :  フレームのロード完成を待つ
# _docGetReadyState:  DOMオブジェクト状態ステータスを取得
#
# TextArea
# getTextArea (name):
# getTextAreaValue(name, attribute):
# getTextAreasValue()：
# setTextArea(name):
# textAreaExists(name):

# Input
# getTextBox(name):
# getTextBoxValue(name, attribute):
# getTextBoxes():
# getTextBoxesValue()
# setTextBox( name, value):
# getInputElements():


# Button
# buttonExists(self, name):
# clickButton(self, name):
# clickButtonImage(self, name):


# Radio
# getRadioButton(name):
# def getRadioButtonSelected(name):
# getRadioButtonValues(name):
# getRadioButtons():

# CheckBox
# checkBoxExists(self, name):

# ListBox
# getListBox(name):
# getListBoxItemCount(name):
# getListBoxOptions(name):
# getListBoxSelected(name):
# getListBoxValue(name, attribute):
# listBoxUnSelect(name, value):
# selectListBox(name, value):


# Image
# getImage( name):
# getImageValue(name, attribute):
# getImages():
# getImagesValue( attribute):
# imageExists(name):


# form
# formExists( name):
# getForm( name=None):
# getFormValue( name, attribute):
# getFormVisibleControlNames( name=None):
# getForms():
# getFormsValue( attribute):

# a
# clickHiddenLink( name):
# getLink( name):
# getLinkValue( name, attribute):
# getLinks( filter=None):

#
# table
# getTable( name):
# getTableData( name):
# getTableRowIndex( name, row):
# getTableText(tableName,rownum,cellnum, frameName=None):
# getTables( filter=None):
# tableCellExists( tableName, cellText):
# tableExists( name):
# tableRowExists( name, row):


#
# div
# divExists( name):
# getDiv( name):
# getDivValue( name, attribute):
# getDivs():
# getDivsValue( attribute):


# clickHiddenElement( element):
# findElement( tag, attributes, val, elementList=None):
# findElementByIndex( tag, indexNum, filter=None, elementList=None):
# findText( text):
# fireElementEvent( tag, controlName, eventName):
# textFinder(text):
# getElementChildren( element, all=True):
# getElementParent( element):
# getElementValue( element, attribute):
# getElementsList( tag, filter=None, elementList=None):

# navigate( url):
# changeWindow( wintext):
# pause( string = "Click to Continue test"):
# goBack(self):
# findWindow( title, indexNum=1):
# closeWindow( title=None):
# refresh(self):
# resize( iWidth, iHeight):
# quit(self):

# getIE(self):
# getPageText(self):
# locationURL(self):
# outerHTML(self):
# randomString( length):