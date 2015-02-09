# This Python file uses the following encoding: utf-8
import urllib2
import exceptions
import string
import re
import time
#システムのディフォルトコードセットをUTF-８に設定、
#でないとASCIIコード直接ファイルに書き込みできない可能性が高いですから、エラー出る
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#---------------------------------------------------------------------------------------------------------
# urlでサイトページのソースを取得する
# url:取得するサイトのURL　charset：サイト側が使用してる文字コードのタイプ「shift_jis」「utf-8」
#作成：wenhao ma 2015/01/21


def get_url_source(url, charset):
    html = None
    try:
        response = urllib2.urlopen(url, timeout=15) #15 secends time out
        html = response.read()
        html = html.decode(charset).encode('utf-8')
    except exceptions.Exception, e:
        print e
    finally:
        return html
#---------------------------------------------------------------------------------------------------------
# プロキシでサイトページのソースを取得する
# url:取得するサイトのURL　charset：サイト側が使用してる文字コードのタイプ「shift_jis」「utf-8」
#作成：wenhao ma 2015/01/21


def get_url_source_by_proxy(url,  proxy_address, charset):
    html = None
    try:
        proxy = {'http': proxy_address}
        proxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        html = urllib2.urlopen(url, timeout=15).read() #15 secends time out ,return false
        html = html.decode(charset).encode('utf-8')
    except exceptions.Exception, e:
        print e
        print proxy_address
        html = None
    finally:
        return html
#---------------------------------------------------------------------------------------------------------
# 文字列を書き込み関数
# filename:ファイル名　writeWords：書き出し文言 TIME_FLAG:0,1
#作成：wenhao ma 2015/01/21


def write_text_to_file_by_utf8(filename, write_words, time_flag=0):
    time_format = '%Y-%m-%d %X'
    if time_flag == 1:
        write_words = time.strftime(time_format, time.localtime()) + '   '+ write_words
    file_handle = file(filename, 'a')
    file_handle.write(write_words)
    file_handle.write("\n")
    file_handle.close
#---------------------------------------------------------------------------------------------------------
#引数で囲まれてる文字列を抽出、開始文字を見つからない場合は””で返して終了
#target_str:対象文字列　start_str:開始文字列　end_str：終了文字列
#作成：wenhao ma 2015/01/21


def get_word_between(target_str,
                     start_str,
                     end_str):
    in_start_word = len(start_str)
    in_end_word = len(end_str)

    if string.find(target_str, start_str) == -1:
        return ""
    else:
        in_start = target_str.find(start_str)+in_start_word
        in_end = target_str.find(end_str, in_start)
        return target_str[in_start:in_end]
#---------------------------------------------------------------------------------------------------------
#引数で囲まれてる文字列を抽出、開始文字を見つからない場合はNoneで返して終了,抽出結果を配列に格納します
#target_str:対象文字列　start_str:開始文字列　end_str：終了文字列
#作成：wenhao ma 2015/01/21


def get_word_between_list(target_str,
                          start_str,
                          end_str):
    in_start_word = len(start_str)
    in_end_word = len(end_str)
    result = []
    search_start = 0

    if target_str.find(start_str) == -1:
        return None
    else:
        while target_str.find(start_str, search_start) != -1:
            in_start = target_str.find(start_str, search_start) + in_start_word
            in_end = target_str.find(end_str, in_start)
            if in_end != -1:
                result.append(target_str[in_start:in_end])
            search_start = in_start
    return result
#---------------------------------------------------------------------------------------------------------
#引数で囲まれてる文字列を抽出、インデックスが引数指定してる結果を返して終了、開始文字を見つからない場合はnullで返して終了,
#target_str:対象文字列　start_str:開始文字列　end_str：終了文字列　index:第X番目の結果
#作成：wenhao ma 2015/01/21


def get_word_between_by_index(target_str,
                              start_str,
                              end_str,
                              index):
    in_start_word = len(start_str)
    in_end_word = len(end_str)
    search_start = 0
    count = 1
    result = ''

    if target_str.find(start_str) == -1:
        return None
    else:
        while target_str.find(start_str, search_start) != -1:
            in_start = target_str.find(start_str, search_start) + in_start_word
            in_end = target_str.find(end_str, in_start)
            if in_end != -1:
                if count == index:
                    result = target_str[in_start:in_end]
                count += 1
            search_start = in_start
    return result
#---------------------------------------------------------------------------------------------------------
#引数で囲まれてる文字列を抽出し、すべての結果を一つの文字列に合併しても戻す。開始文字を見つからない場合は""で返して終了,
#target_str:対象文字列　start_str:開始文字列　end_str：終了文字列
#作成：wenhao ma 2015/01/21


def get_word_between_to_total_string(target_str,
                                     start_str,
                                     end_str):
    result_list = get_word_between_list(target_str, start_str, end_str)
    if result_list is None:
        result_str = ''
    else:
        result_str = "/".join(result_list)
    return result_str
#---------------------------------------------------------------------------------------------------------
#対象文字列から正規表現で検索文字列を探します。見つかったら結果配列を返す、見つからない場合はNoneで返して終了,
#target_str:対象文字列　pattern_key：検索正規表現の規則
#作成：wenhao ma 2015/01/22


def search_key_words_list_by_regex(target_str,
                                   pattern_key):
    match_list = None
    matches = re.findall(pattern_key, target_str)
    if len(matches) > 0:
        match_list = matches
    return match_list
#---------------------------------------------------------------------------------------------------------
#対象文字列から正規表現で検索文字列を探します。見つかったら結果を指定したワードを入れ替えて返す、見つからない場合は元文字列を返して終了,
#target_str:対象文字列　pattern_key：検索正規表現の規則
# replace_str:入れ替える文字列 count:入れ替えの数（第一あった結果からcountまで入れ替え）その以外の場合： すべて入れ替える
#作成：wenhao ma 2015/01/22


def replace_str_by_regex_count(target_str,
                               pattern_key,
                               replace_str,
                               count=0):
    result_str = ''
    result_str = re.sub(pattern_key, replace_str, target_str, count)
    return result_str
#--------------------------------------------------------------------------------------------------------
#対象文字列から正規表現で検索文字列を探します。見つかったら結果のリストにインデックスが指定した数値とあったら入れ替える
#target_str:対象文字列　pattern_key：検索正規表現の規則
# index:範囲「１からマッチ数まで」、範囲外の場合は入れ替えない。マイナス値を指定する場合、最後から数える
#作成：wenhao ma 2015/01/22


def string_join(replace_str,
                match_list,
                split_list,
                index):
    count = 0
    result_str = ""
    while count <= len(split_list) - 1:
        if count <= len(match_list) - 1:
            if count == index:
                result_str = result_str + split_list[count] + replace_str
            else:
                result_str = result_str + split_list[count] + match_list[count]
        else:
            result_str = result_str + split_list[count]
        count += 1
    return result_str


def replace_str_by_regex_index(target_str,
                               pattern_key,
                               replace_str,
                               index):
    split_list = re.split(pattern_key, target_str)
    match_list = re.findall(pattern_key, target_str)
    match_num = len(match_list)

    if match_num < int(abs(index)) or index == 0:
        return target_str
    elif index > 0:
        return string_join(replace_str, match_list, split_list, index - 1)
    else:
        return string_join(replace_str, match_list, split_list, match_num + index)
#--------------------------------------------------------------------------------------------------------
