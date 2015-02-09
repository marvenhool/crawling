# This Python file uses the following encoding: utf-8
# abc
import crawling_module
import time
import random
import urllib2
import exceptions
import string
import re
#####システムのディフォルトコードセットをUTF-８に設定、
#####でないとASCIIコード直接ファイルに書き込みできない可能性が高いですから、エラー出る
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


#-------------------------------------#TESTCODE START#----------------------------------------------------
# buf = crawling_module.get_url_source('http://www.bengo4.com/tokyo/', 'UTF-8')
#print buf

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

# buf = crawling_module.get_url_source('http://tabelog.com/tokyo/A1307/A130701/', 'UTF-8')

# buf = crawling_module.get_url_source_by_proxy('http://tabelog.com/tokyo/A1307/A130701/', 'http://117.135.252.14:84', 'UTF-8')
# print buf

#使えるプロキシ： http://60.55.49.9:3128

# write_data_to_file_by_url('http://tabelog.com/tokyo/A1307/A130701/13000005/', 'http://120.198.243.82:80')

#-------------------------------------#TESTCODE END#----------------------------------------------------

def proxy_test(proxy_list):

    for proxy in proxy_list:
        buf = get_url_source_by_proxy('http://tabelog.com/tokyo/A1307/A130701/13000005/', proxy, 'UTF-8')
        if buf is None:
            pass
        elif buf.find('アクセスが制限されています') != -1:
            pass
        else:
            crawling_module.write_text_to_file_by_utf8('useful_proxy.csv', proxy, 0)



def get_url_source_by_proxy(url,  proxy_address, charset):
    html = None
    try:
        proxy = {'http': proxy_address}
        proxy_handler = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        html = urllib2.urlopen(url, timeout=5).read() #5 secends time out ,return false
        html = html.decode(charset).encode('utf-8')
    except exceptions.Exception, e:
        print e
        print proxy_address
        html = None
    finally:
        return html

proxy_list = ['http://1.34.220.170:8088','http://101.227.252.130:8081','http://101.4.136.34:9999','http://101.71.27.27:8000','http://110.4.12.173:80','http://110.78.155.132:80','http://111.1.36.133:80','http://111.1.36.6:80','http://111.1.61.23:8080','http://111.12.128.166:80','http://112.170.72.132:3128','http://113.105.224.87:80','http://113.207.128.129:80','http://113.207.129.129:80','http://114.34.148.204:3128','http://117.135.194.53:80','http://117.135.250.51:80','http://117.135.250.51:82','http://117.135.250.51:86','http://117.135.250.53:80','http://117.135.250.54:80','http://117.135.250.54:84','http://117.135.250.55:80','http://117.135.250.56:80','http://117.135.250.68:80','http://117.135.250.83:80','http://117.135.250.84:80','http://117.135.250.86:80','http://117.135.250.9:80','http://117.135.251.74:82','http://117.135.251.76:82','http://117.135.251.78:80','http://117.135.252.14:80','http://117.135.252.14:82','http://117.135.252.14:84','http://117.149.213.212:8123','http://117.177.243.79:80','http://119.40.98.26:8080','http://120.126.50.118:9064','http://120.131.128.209:80','http://120.193.146.95:843','http://120.197.234.166:80','http://120.198.243.131:80','http://120.202.249.230:80','http://121.243.51.107:80','http://121.42.138.65:3128','http://123.110.121.135:8088','http://123.125.19.44:80','http://123.138.185.50:80','http://123.194.41.185:8088','http://123.195.131.10:8088','http://123.195.192.152:9064','http://124.11.129.123:8088','http://124.88.67.13:83','http://142.54.170.72:3127','http://142.54.170.72:7808','http://159.8.36.242:3128','http://162.208.49.45:8089','http://175.43.20.95:80','http://177.69.195.4:3128','http://180.248.17.135:3128','http://182.239.127.134:80','http://183.207.224.50:80','http://183.207.224.50:81','http://183.207.224.50:82','http://183.207.224.50:85','http://183.207.224.51:80','http://183.207.224.51:83','http://183.207.224.51:84','http://183.207.224.52:80','http://183.207.224.52:81','http://183.207.228.115:80','http://183.207.228.122:80','http://183.207.228.123:80','http://183.207.228.22:80','http://183.207.228.22:82','http://183.207.228.22:84','http://183.207.228.22:85','http://183.207.228.22:86','http://183.207.228.23:80','http://183.207.228.23:81','http://183.207.228.23:85','http://183.207.228.23:86','http://183.207.228.42:80','http://183.207.228.44:80','http://183.207.228.50:80','http://183.207.228.50:81','http://183.207.228.50:82','http://183.207.228.50:83','http://183.207.228.50:84','http://183.207.228.51:80','http://183.207.228.51:82','http://183.207.228.51:83','http://183.207.228.52:80','http://183.207.228.52:83','http://183.207.228.52:84','http://183.207.228.52:85','http://183.207.228.54:80','http://183.207.228.57:80','http://183.207.228.58:80','http://183.207.229.15:80','http://183.224.1.30:80','http://185.72.156.19:3127','http://199.200.120.37:7808','http://200.90.106.52:9064','http://202.106.16.36:3128','http://202.119.25.69:9999','http://202.171.253.74:86','http://203.151.21.184:3128','http://203.192.10.66:80','http://212.112.124.137:8080','http://217.21.43.237:3128','http://218.65.132.45:8081','http://219.246.90.162:3128','http://219.93.183.106:8080','http://222.171.28.121:3128','http://222.87.129.218:843','http://223.83.211.203:8123','http://31.25.142.216:3128','http://36.250.74.88:8103','http://41.205.231.202:8080','http://41.216.159.158:8080','http://58.242.249.14:33942','http://58.242.249.52:17657','http://58.251.78.71:8088','http://58.99.120.122:8088','http://60.244.66.86:8088','http://60.55.49.9:3128','http://61.54.221.200:3128','http://61.70.110.151:8088','http://69.197.148.18:3127','http://69.197.148.18:7808','http://69.197.148.18:8089','http://80.63.55.3:8080','http://83.241.46.175:8080','http://86.107.110.73:3127','http://88.132.82.236:8088','http://91.121.108.174:3128']

proxy_test(proxy_list)













