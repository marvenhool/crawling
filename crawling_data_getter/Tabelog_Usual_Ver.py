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

###同じIPで取得最大NUM
MAX_NUMBER = 100
####連続アクセスエラー数フラグ
ACCESS_ERROR_COUNT = 0
#####現在使っているプロキシ
PROXY = ''

####関数write_data_page_by_page：ページにある店舗情報を取得、結果ファイルに書き込み

def write_data_to_file_by_url(data_page_url, PROXY):
    
    global ACCESS_ERROR_COUNT
    buf = crawling_module.get_url_source_by_proxy(data_page_url, PROXY, 'utf-8')
    crawling_module.write_text_to_file_by_utf8('logger.csv', data_page_url + 'にアクセス完了しました。' ,1)

    if buf is not None and buf.find('お探しのページが見つかりません。') == -1:

        #####顧客名
        custom_name = crawling_module.get_word_between(buf,  '<p class="mname"><strong>', '</strong>')
        custom_name = custom_name.replace('</strong>', '')
        custom_name = custom_name.replace('</p>', '')
        custom_name = "".join(custom_name.split())
        if custom_name == '':
            custom_name = crawling_module.get_word_between(buf,  '<span class="display-name">', '</span>')
            custom_name = custom_name.replace('</strong>', '')
            custom_name = custom_name.replace('</p>', '')
            custom_name = "".join(custom_name.split())

        #####口コミ数
        comment = crawling_module.get_word_between(buf, '<em class="num" property="v:count">', '</em>')
        comment = comment.replace('<dd>', '')
        comment = "".join(comment.split())

        #####カナ
        furikana = crawling_module.get_word_between(buf, '<p class="mname"><strong>', '</p>')
        furikana = crawling_module.get_word_between(furikana, '（', '）')
        furikana = furikana.replace('<dd>', '')
        furikana = "".join(furikana.split())

        #####CENA予約可否
        net_booking = ''
        if buf.find('_side_calendar_widget.js?1422849891') == -1:
            net_booking = 'ネット予約不可'
        else:
            net_booking = 'ネット予約可'

        #####閉店チェック
        shop_status = ''
        if buf.find( 'このお店は現在閉店しております') == -1:
            if buf.find( 'rst-status-badge-large rst-st-pending')==-1:
                shop_status = '営業中'
            else:
                shop_status = '掲載保留'
        else:
            shop_status = '閉店'

        #####会員状況
        membership = ''
        if buf.find('このレストランは食べログ店舗会員に登録しているため、ユーザの皆様は編集することができません。') != -1:
            if buf.find('<div class="listing">') != -1:
                membership = '無料会員'
            else:
                membership = '有料会員'
        else:
            membership = '非会員'

        #####ジャンル
        genre = crawling_module.get_word_between_to_total_string(buf, '<span property="v:category">', '</span>')
        genre = genre.replace('<dd>', '')
        genre = "".join(genre.split())

        #####電話/IP電話
        tel = ''
        ipp = ''
        if shop_status =='閉店':
            tel = ''
        else:
            tel = crawling_module.get_word_between(buf,'<p class="ppc-sub">', '</strong>')
            tel = tel.replace('<strong>', '')
            tel = "".join(tel.split())

            ipp = crawling_module.get_word_between(buf,'<strong property="v:tel">', '</strong>')
            ipp = ipp.replace('<strong>', '')
            ipp = "".join(ipp.split())

            if tel == '':
                tel = ipp
                ipp = ''

        #####最寄り駅
        station = crawling_module.get_word_between(buf, '<th>交通手段</th>', '</td>')
        station = station.replace('<td>', '')
        station = station.replace('<p>', '')
        station = station.replace('</p>', '')
        station = "".join(station.split())

        #####総スコア
        total_score = crawling_module.get_word_between(buf, '<strong class="score" rel="v:rating"><span property="v:average">', '</span>')
        total_score = total_score.replace('<dd>', '')
        total_score = "".join(total_score.split())

        #####昼スコア
        day_score = crawling_module.get_word_between(buf, '<span class="lunch">昼の点数：</span><em>', '</em>')
        day_score = day_score.replace('<dd>', '')
        day_score = "".join(day_score.split())

        #####夜スコア
        night_score = crawling_module.get_word_between(buf, '<span class="dinner">夜の点数：</span><em>', '</em>')
        night_score = night_score.replace('<dd>', '')
        night_score = "".join(night_score.split())

        #####通常予約可否
        if buf.find('予約可') == -1:
            if buf.find('予約不可') == -1:
                booking = ''
            else:
                booking = '予約不可'
        else:
             booking = '予約可'


        #####住所
        address = crawling_module.get_word_between(buf, '<p rel="v:addr">', '</p>')
        address = address.replace('<span property="v:region">', '')
        address = address.replace('<span property="v:locality">', '')
        address = address.replace('<span property="v:street-address">', '')
        address = address.replace('</span>', '')
        address = address.replace('</a>', '')
        address = crawling_module.replace_str_by_regex_count(address, '<a href="/\w*/" class="listlink">', '',)
        address = crawling_module.replace_str_by_regex_count\
            (address, '<a href="/\w*/\w*/" class="listlink">', '',)
        address = crawling_module.replace_str_by_regex_count\
            (address, '<a href="/\w*/\w*/\w*/" class="listlink">', '',)
        address = crawling_module.replace_str_by_regex_count\
            (address, '<a href="/\w*/\w*/\w*/\w*/" class="listlink">', '',)


        #####経緯度
        geoCode = crawling_module.get_word_between(buf, 'center=', '&amp;markers=')
        geoCode = geoCode.replace('<dd>', '')
        geoCode = "".join(geoCode.split())

        #####営業時間
        open_time = crawling_module.get_word_between(buf, '<th>営業時間</th>', '</td>')
        open_time = open_time.replace('<td>', '')
        open_time = open_time.replace('<p>', '')
        open_time = open_time.replace('</p>', '')
        open_time = "".join(open_time.split())

        #####平均予算昼
        day_cost = crawling_module.get_word_between(buf,  '[昼]</span><span class="price">', '</span>')
        day_cost = day_cost.replace('<dd>', '')
        day_cost = "".join(day_cost.split())

        #####平均予算夜
        night_cost = crawling_module.get_word_between(buf, '[夜]</span><span class="price">', '</span>')
        night_cost = night_cost.replace('<dd>', '')
        night_cost = "".join(night_cost.split())

        #####席数
        seats = crawling_module.get_word_between(buf, '<th>席数</th>', '</td>')
        seats = seats.replace('</strong>', '')
        seats = seats.replace('<strong>', '')
        seats = seats.replace('<td>', '')
        seats = seats.replace('<p>', '')
        seats = seats.replace('</p>', '')
        seats = "".join(seats.split())

        #####クーポン
        if buf.find('<strong>お得なクーポン</strong>') == -1:
            coupon ='クーポン情報なし'
        else:
            coupon = 'クーポン情報あり'

        #####定休日
        holiday = crawling_module.get_word_between(buf, '<th>定休日</th>', '</td>')
        holiday = holiday.replace('<dd>', '')
        holiday = holiday.replace('<td>', '')
        holiday = holiday.replace('<p>', '')
        holiday = holiday.replace('</p>', '')
        holiday = "".join(holiday.split())

        #####クレカ
        credit_card = crawling_module.get_word_between(buf, '<th>カード</th>', '</td>')
        credit_card = credit_card.replace('<strong>', '')
        credit_card = credit_card.replace('<td>', '')
        credit_card = credit_card.replace('<p>', '')
        credit_card = credit_card.replace('</p>', '')
        credit_card = "".join(credit_card.split())

        #####URL
        #####data_page_url

        #####総PV数
        PV_total = crawling_module.get_word_between(buf, 'アクセス数 <em>', '</em>')
        PV_total = PV_total.replace('<dd>', '')
        PV_total = PV_total.replace('<td>', '')
        PV_total = PV_total.replace('<p>', '')
        PV_total = PV_total.replace('</p>', '')
        PV_total = "".join(PV_total.split())

        #####先週PV数
        PV_last_week = crawling_module.get_word_between(buf, '先週のアクセス数：</span><em>', '</em>')
        PV_last_week = PV_last_week.replace('<dd>', '')
        PV_last_week = PV_last_week.replace('<td>', '')
        PV_last_week = PV_last_week.replace('<p>', '')
        PV_last_week = PV_last_week.replace('</p>', '')
        PV_last_week = "".join(PV_last_week.split())

         #####先々週PV数
        PV_last_week_before = crawling_module.get_word_between(buf, '先々週のアクセス数：</span><em>', '</em>')
        PV_last_week_before = PV_last_week_before.replace('<dd>', '')
        PV_last_week_before = PV_last_week_before.replace('<td>', '')
        PV_last_week_before = PV_last_week_before.replace('<p>', '')
        PV_last_week_before = PV_last_week_before.replace('</p>', '')
        PV_last_week_before = "".join(PV_last_week_before.split())

        #####プレーミアムクーポン有無
        if buf.find('<span class="pcoupon-item-lead">') == -1:
            pre_coupon ='プレーミアムクーポン情報なし'
        else:
            pre_coupon = 'プレーミアムクーポン情報あり'


        #####県域コード
        tempstr = data_page_url.replace('http://tabelog.com/tokyo/A1307/A130701/', '')
        if len(tempstr) == 7:
            province_code = tempstr[:1]
        else:
            province_code = tempstr[:2]

        #####公式情報有無
        if buf.find('<a class="official-badge">公式情報あり</a>') == -1:
            official_news ='公式情報なし'
        else:
            official_news = '公式情報あり'

        result_str = '"' + custom_name + '","' + comment + '","' + furikana + '","' + net_booking + '","' + shop_status \
                     + '","' + membership + '","' + genre + '","' + tel + '","' + ipp + '","' + station\
                     + '","' + total_score + '","' + day_score + '","' + night_score + '","' + booking\
                     + '","' + address + '","' + geoCode + '","' + open_time + '","' + day_cost \
                     + '","' + night_cost + '","' + seats + '","' + coupon + '","' + holiday\
                     + '","' + credit_card + '","' + data_page_url + '","' + PV_total + '","' + PV_last_week \
                     + '","' + PV_last_week_before + '","' + pre_coupon + '","' + province_code + '","' + official_news+ '"'

        crawling_module.write_text_to_file_by_utf8(province_code +'.csv', result_str)
        ACCESS_ERROR_COUNT = 0
    else:
        crawling_module.write_text_to_file_by_utf8('logger.csv', data_page_url + 'が見つかりませんでした。',1)
        ACCESS_ERROR_COUNT += 1

#######================================================食べログ==============================================================

####### randomで使えるプロキシをゲット、プロキシが接続できるかどうかをテスト、使える場合繰り返し終わり
def proxy_change(proxy_list):
    result = None
    buf = None
    max = len(proxy_list) - 1
    while buf is None:
        result = proxy_list[random.randint(0, max)]
        buf = crawling_module.get_url_source_by_proxy('http://tabelog.com/tokyo/A1307/A130701/13000005/', result, 'UTF-8')
        if buf is not None:
            if buf.find('アクセスが制限されています') != -1:
                buf = None
    return result

####プロキシリスト
proxy_list = ['http://101.227.252.130:8081','http://101.4.136.34:9999','http://101.69.180.85:80','http://101.71.27.120:80','http://101.71.27.27:8000','http://103.246.244.161:44338','http://109.107.133.46:8080','http://109.224.45.205:8080','http://110.4.12.173:80','http://110.4.12.178:80','http://110.4.24.176:80','http://110.4.24.178:80','http://111.1.36.10:80','http://111.1.36.130:80','http://111.1.36.133:80','http://111.1.36.6:80','http://111.1.61.23:8080','http://111.12.128.135:80','http://111.12.128.166:80','http://111.12.128.167:80','http://111.12.128.171:80','http://111.12.128.171:8060','http://111.12.128.171:8080','http://111.12.128.171:83','http://111.12.128.171:9000','http://111.12.128.171:9064','http://111.12.128.171:9797','http://111.12.128.172:80','http://111.12.128.172:8080','http://111.12.128.172:8085','http://111.12.128.172:8088','http://111.12.128.172:8089','http://111.12.128.172:81','http://111.13.136.58:843','http://111.13.65.124:80','http://111.13.65.125:80','http://111.206.50.177:80','http://111.206.81.248:80','http://113.105.224.87:80','http://113.207.128.129:80','http://113.207.129.129:80','http://113.207.130.166:80','http://113.214.13.1:8000','http://113.255.97.186:80','http://114.6.52.130:8080','http://114.80.182.132:80','http://115.231.96.120:80','http://115.238.225.26:80','http://116.50.25.181:8585','http://117.135.194.53:80','http://117.135.250.11:80','http://117.135.250.51:80','http://117.135.250.51:82','http://117.135.250.51:86','http://117.135.250.54:80','http://117.135.250.54:82','http://117.135.250.54:84','http://117.135.250.55:80','http://117.135.250.55:81','http://117.135.250.55:82','http://117.135.250.56:80','http://117.135.250.68:86','http://117.135.250.83:80','http://117.135.250.84:80','http://117.135.250.9:80','http://117.135.251.74:80','http://117.135.251.74:82','http://117.135.251.75:80','http://117.135.251.75:82','http://117.135.251.76:80','http://117.135.251.76:82','http://117.135.251.78:80','http://117.135.251.78:82','http://117.135.252.14:80','http://117.135.252.14:81','http://117.135.252.14:82','http://117.135.252.14:84','http://117.52.97.210:3128','http://117.79.64.84:80','http://118.163.165.250:3128','http://118.174.10.193:3128','http://119.110.81.101:3128','http://119.40.98.26:8080','http://119.90.127.2:80','http://119.90.127.5:80','http://120.131.128.209:80','http://120.192.249.74:80','http://120.193.146.95:843','http://120.197.234.166:80','http://120.198.243.116:80','http://120.198.243.118:80','http://120.198.243.130:80','http://120.198.243.131:80','http://120.198.243.14:80','http://120.198.243.15:80','http://120.198.243.3:80','http://120.198.243.50:80','http://120.198.243.51:80','http://120.198.243.52:80','http://120.198.243.53:80','http://120.198.243.54:80','http://120.198.243.82:80','http://120.198.243.83:80','http://120.198.243.86:80','http://120.236.148.113:3128','http://121.243.51.107:80','http://123.1.175.43:8080','http://123.110.105.61:8088','http://123.110.75.213:9064','http://123.125.19.44:80','http://123.138.185.50:80','http://124.248.190.220:8080','http://124.88.67.13:83','http://124.88.67.13:843','http://124.95.163.102:80','http://125.24.79.197:80','http://125.88.193.205:80','http://125.88.215.120:80','http://128.199.77.145:3128','http://139.0.25.146:8080','http://14.199.114.63:8088','http://140.125.47.102:9064','http://159.8.36.242:3128','http://162.208.49.45:8089','http://165.132.27.110:8080','http://175.43.20.95:80','http://177.69.195.4:3128','http://177.84.241.107:3128','http://180.153.100.242:80','http://180.153.100.242:84','http://180.153.100.242:86','http://180.177.71.18:9064','http://182.118.31.46:80','http://182.16.15.26:3128','http://182.235.184.16:8088','http://182.239.127.134:80','http://182.239.127.136:80','http://182.239.127.137:80','http://182.239.127.139:80','http://182.239.127.139:81','http://182.239.127.139:82','http://182.239.127.140:80','http://182.239.127.140:81','http://182.239.127.140:82','http://182.239.95.134:80','http://182.239.95.136:80','http://182.239.95.137:80','http://182.239.95.139:80','http://182.253.33.129:3128','http://183.207.224.12:80','http://183.207.224.13:80','http://183.207.224.42:80','http://183.207.224.43:80','http://183.207.224.44:80','http://183.207.224.45:80','http://183.207.224.50:80','http://183.207.224.50:81','http://183.207.224.50:82','http://183.207.224.50:84','http://183.207.224.50:85','http://183.207.224.50:86','http://183.207.224.51:80','http://183.207.224.51:81','http://183.207.224.51:83','http://183.207.224.51:84','http://183.207.224.51:86','http://183.207.224.52:80','http://183.207.224.52:81','http://183.207.224.52:82','http://183.207.228.115:80','http://183.207.228.116:80','http://183.207.228.117:80','http://183.207.228.119:80','http://183.207.228.122:80','http://183.207.228.123:80','http://183.207.228.22:80','http://183.207.228.22:81','http://183.207.228.22:82','http://183.207.228.22:83','http://183.207.228.22:84','http://183.207.228.22:85','http://183.207.228.22:86','http://183.207.228.44:80','http://183.207.228.50:80','http://183.207.228.50:81','http://183.207.228.50:82','http://183.207.228.50:83','http://183.207.228.50:84','http://183.207.228.51:80','http://183.207.228.51:82','http://183.207.228.51:83','http://183.207.228.51:85','http://183.207.228.52:80','http://183.207.228.52:83','http://183.207.228.52:84','http://183.207.228.52:85','http://183.207.228.54:80','http://183.207.228.54:82','http://183.207.228.54:83','http://183.207.228.56:80','http://183.207.228.57:80','http://183.207.228.58:80','http://183.207.228.60:80','http://183.207.229.15:80','http://183.207.229.17:80','http://183.207.229.19:8081','http://183.207.229.19:81','http://183.207.229.19:82','http://183.207.229.19:9090','http://183.207.237.11:80','http://183.224.1.30:80','http://183.89.225.240:3128','http://190.10.156.194:8888','http://190.121.230.148:8080','http://190.52.192.1:8080','http://195.114.129.171:3128','http://199.200.120.37:7808','http://200.109.230.138:80','http://200.109.230.139:80','http://200.109.230.140:80','http://200.109.230.141:80','http://200.30.202.238:8080','http://202.102.27.72:80','http://202.106.16.36:3128','http://202.119.25.227:9999','http://202.119.25.69:9999','http://202.119.25.70:9999','http://202.119.25.71:9999','http://202.119.25.72:9999','http://202.138.233.145:8080','http://202.171.253.74:86','http://202.28.120.10:8080','http://202.43.191.114:3128','http://202.49.183.14:8080','http://202.77.115.71:54321','http://202.99.16.28:3128','http://203.151.21.184:3128','http://203.176.140.226:8080','http://203.192.10.66:80','http://203.70.194.170:8080','http://209.177.93.6:80','http://210.101.131.231:8080','http://210.101.131.232:8080','http://210.52.217.97:80','http://211.162.0.170:80','http://218.188.16.123:8080','http://218.207.195.206:8000','http://218.207.195.206:8080','http://218.27.136.164:8081','http://218.65.132.45:8081','http://219.246.65.143:3128','http://219.246.90.162:3128','http://219.93.183.106:8080','http://221.12.173.130:3128','http://221.130.199.222:80','http://221.130.199.224:80','http://221.181.73.45:80','http://221.193.249.140:3128','http://222.124.196.42:8080','http://222.124.218.83:8080','http://222.73.233.134:80','http://222.73.233.135:80','http://222.73.233.136:80','http://223.18.140.82:8088','http://223.82.245.168:80','http://223.86.66.223:8123','http://31.25.142.216:3128','http://36.250.74.88:8103','http://41.160.80.194:80','http://41.190.57.175:8080','http://41.207.40.22:3128','http://41.216.159.158:8080','http://41.222.196.52:8080','http://41.78.208.90:8080','http://41.79.71.40:8080','http://49.1.245.234:3128','http://49.1.245.237:3128','http://49.1.245.238:3128','http://5.56.61.26:12313','http://58.242.249.14:33942','http://58.242.249.52:17657','http://58.246.199.122:3128','http://58.251.78.71:8088','http://58.65.241.226:8080','http://58.96.181.169:3128','http://58.99.120.122:8088','http://59.124.241.199:8080','http://60.213.189.170:3988','http://60.55.49.9:3128','http://61.133.116.37:3128','http://61.156.35.2:3128','http://61.163.165.250:9797','http://61.184.192.42:80','http://61.53.143.179:80','http://61.54.221.200:3128','http://62.205.216.247:21320','http://62.82.58.99:8080','http://66.225.231.173:7808','http://69.197.148.18:3127','http://69.197.148.18:7808','http://69.197.148.18:8089','http://80.95.113.66:3128','http://82.144.204.41:3128','http://82.99.180.106:3128','http://86.107.110.73:3127','http://86.107.110.73:7808','http://88.132.82.236:8088','http://91.139.246.123:9064','http://91.196.48.196:9999','http://93.191.133.247:4444','http://94.242.238.5:443']


PROXY = proxy_change(proxy_list)
crawling_module.write_text_to_file_by_utf8('logger.csv', '現在使用してるプロキシは'+PROXY , 1)


#####開始県域を設定
i=1000000

while i <= 3000000:  ####エンド県域を設定

    #######プロキシの変更が必要かどうかを判断
    if i%MAX_NUMBER == 0:
        PROXY = proxy_change(proxy_list)
        crawling_module.write_text_to_file_by_utf8('logger.csv', '現在使用してるプロキシは'+PROXY,1)

    #######データを取得し、ファイルに書き込み
    if PROXY is not None:
        shop_url ='http://tabelog.com/tokyo/A1307/A130701/' + str(i)
        write_data_to_file_by_url(shop_url, PROXY)


    #####連続エラーアクセス数がM上限を超えた場合、次の県域を取得開始
    temp_str = str(i)
    if ACCESS_ERROR_COUNT <= 50:
        i += 1
    else:
        temp_length = len(str(i))
        if temp_length == 7:
            temp_str = temp_str[:1]
            i = (int(temp_str) + 1)*1000000
            ACCESS_ERROR_COUNT = 0
        else:
            temp_str = temp_str[:2]
            i = (int(temp_str) + 1)*1000000
            ACCESS_ERROR_COUNT = 0