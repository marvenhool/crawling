# This Python file uses the following encoding: utf-8
# abc
import crawling_module

# #-----------------------------------------------------------------------------------------------
#関数write_data_page_by_page：一覧ページから店舗のURLを収集し、データを取得関数を呼び出す

def write_data_page_by_page(total_page_url):
    buf = crawling_module.get_url_source_by_proxy(total_page_url, 'http://202.106.16.36:3128', 'UTF-8')
    crawling_module.write_text_to_file_by_utf8('logger.csv', total_page_url + 'にアクセス完了しました。')
    url_list = crawling_module.get_word_between_list(buf, '<div class="photo">', '">')

    if url_list is None:
        crawling_module.write_text_to_file_by_utf8('logger.csv', 'クローリングできるURLをみつかりませんでした')
    else:
        for url in url_list:
            url = "".join(url.split())
            url = url.replace('<atarget="_blank"href="', '')
            url = 'http://www.bengo4.com/' + url
            write_data_to_file_by_url(url)
    return True
# #-----------------------------------------------------------------------------------------------
# #関数write_data_page_by_page：ページにある店舗情報を取得、結果ファイルに書き込み

def write_data_to_file_by_url(data_page_url):

    buf = crawling_module.get_url_source_by_proxy(data_page_url, 'http://202.106.16.36:3128', 'UTF-8')
    crawling_module.write_text_to_file_by_utf8('logger.csv', data_page_url + 'にアクセス完了しました。')

    custom_name = crawling_module.get_word_between(buf, '<dt>名前</dt>', '</dd>')
    custom_name = custom_name.replace('<dd>', '')
    custom_name = "".join(custom_name.split())

    result_str = '"' + custom_name + '","' + data_page_url + '"'
    crawling_module.write_text_to_file_by_utf8('result.csv', result_str)
# #-----------------------------------------------------------------------------------------------
#クローラーの実行はすべてここから

print '取得開始します。'
touken_list = ['hiroshima']
k = 1
for touken in touken_list:
    ichi_url = 'http://www.bengo4.com/' + touken
    buf = crawling_module.get_url_source_by_proxy('http://www.bengo4.com/tokyo/', 'http://202.106.16.36:3128', 'UTF-8')
    number_str = crawling_module.get_word_between(buf, '<span class="number_item">', '</span>')

    if number_str != "" and number_str != '0':
        number_str = number_str.replace(',', '')
        num = long(number_str)
        page = num/30 + 1
        while k <= page:
            temp_url = 'http://www.bengo4.com/' + touken + '/?page=' + str(k)
            write_data_page_by_page(temp_url)
            k += 1

print '実行完了しました。'

#ここまで実行完了

#-----------------------------------------TESTCODE START----------------------------------------------
#testCode start
# buf = crawling_module.get_url_source('http://www.bengo4.com/tokyo/', 'UTF-8')
#print buf

#crawling_module.UnicodeWriteTextFile('buf.csv', buf)
# getword = crawling_module.get_word_between_to_total_string(buf, '<a target="_blank1111" class="uaLbl_111" href="', '">')

# buf = crawling_module.get_url_source_by_proxy('http://www.bengo4.com/tokyo/', 'http://202.106.16.36:3128', 'UTF-8')
# print buf

#Regex test Start
# result = crawling_module.replace_str_by_regex_index('にち1幅get広く　にち2ひ　getやが　にち334get', 'にち\d','===',-4)
# print result
# print result[0]
# print result[1]
# print result[2]
#Regex test End

# result = crawling_module.ReplaceStrByRegexIndex( 'にち1幅広くにち2ひやがにち3にち4㈰にち2ｘにち5','にち\d','===',-3)

# buf = crawling_module.get_url_source('http://www.baidu.com/s?wd=ip', 'UTF-8')
#buf = crawling_module.get_url_source_by_proxy('http://tabelog.com/hokkaido/A0105/A010501/1001279/', 'http://202.106.16.36:3128', 'UTF-8')
#print buf

#-----------------------------------------TESTCODE END----------------------------------------------