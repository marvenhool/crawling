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
ACCESS_COUNT = 0
#####現在使っているプロキシ
PROXY = ''

####関数write_data_page_by_page：ページにある店舗情報を取得、結果ファイルに書き込み

def write_data_to_file_by_url(data_page_url, PROXY):

    buf = crawling_module.get_url_source_by_proxy(data_page_url, PROXY, 'utf-8')
    crawling_module.write_text_to_file_by_utf8('logger.csv', data_page_url + 'にアクセス完了しました。' ,1)

    if buf is None or buf.find('お探しのページが見つかりません。') == -1:

        #取得できてるかを判断し、固定プロキシIPでもう一回再取得してみます。
        if buf is None or buf.find('アクセスが制限されています') != -1 or (buf.find('<p class="mname">') == -1 and buf.find('<span class="display-name">') == -1):
            crawling_module.write_text_to_file_by_utf8('logger.csv', data_page_url + 'を別プロキシで再取得しています' ,1)
            buf = crawling_module.get_url_source_by_proxy(data_page_url, "http://120.198.243.86:80", 'utf-8')

        #これでもできない場合、本機IPで再取得してみます。
        if buf is None or buf.find('アクセスが制限されています') != -1 or (buf.find('<p class="mname">') == -1 and buf.find('<span class="display-name">') == -1):
            crawling_module.write_text_to_file_by_utf8('logger.csv', data_page_url + 'を本機IPで再取得しています' ,1)
            buf = crawling_module.get_url_source(data_page_url, 'utf-8')

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
            if buf.find( 'rst-status-badge-large rst-st-pending') == -1:
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
        if shop_status == '閉店':
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
            official_news = '公式情報なし'
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
    else:
        crawling_module.write_text_to_file_by_utf8('logger.csv', data_page_url + 'が見つかりませんでした。',1)

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
proxy_list = ['http://101.255.74.58:8080','http://101.4.136.34:9999','http://101.69.180.85:443','http://101.69.180.85:80','http://101.71.27.120:80','http://101.79.241.40:8080','http://103.246.244.161:44338','http://103.3.78.218:8080','http://106.186.123.92:3128','http://106.187.43.78:3128','http://109.196.127.35:8888','http://110.138.179.12:3128','http://110.169.186.75:3128','http://110.173.0.58:80','http://110.173.0.58:8080','http://110.4.12.173:80','http://110.4.12.178:80','http://111.1.32.118:8080','http://111.1.36.133:80','http://111.1.36.6:80','http://111.12.128.135:80','http://111.12.128.166:80','http://111.12.128.167:80','http://111.12.128.171:80','http://111.12.128.171:8001','http://111.12.128.171:8060','http://111.12.128.171:8080','http://111.12.128.171:83','http://111.12.128.171:9000','http://111.12.128.171:9064','http://111.12.128.171:9797','http://111.12.128.172:80','http://111.12.128.172:8080','http://111.12.128.172:8085','http://111.12.128.172:8085','http://111.12.128.172:8088','http://111.12.128.172:8089','http://111.12.128.172:81','http://111.13.136.58:80','http://111.13.136.58:843','http://111.13.136.59:80','http://111.13.136.59:843','http://111.193.66.195:9000','http://111.193.71.113:9000','http://111.206.50.177:80','http://111.206.81.248:80','http://112.105.11.194:8088','http://112.18.63.8:8123','http://112.78.1.36:3128','http://113.105.224.87:80','http://114.6.34.194:8080','http://114.6.52.130:8080','http://114.80.182.132:80','http://115.231.96.120:80','http://115.238.225.26:80','http://117.102.163.5:80','http://117.135.194.53:80','http://117.135.252.14:80','http://117.135.252.14:81','http://117.135.252.14:82','http://117.135.252.14:84','http://117.164.54.164:8123','http://117.167.64.196:8123','http://117.59.224.106:80','http://117.59.224.106:8080','http://117.79.64.86:80','http://119.40.98.26:8080','http://119.6.144.74:80','http://119.6.144.74:81','http://119.6.144.74:82','http://119.6.144.74:83','http://119.90.127.3:80','http://119.90.127.5:80','http://120.131.128.209:80','http://120.131.128.211:80','http://120.192.249.74:80','http://120.193.146.95:81','http://120.193.146.95:82','http://120.193.146.95:83','http://120.193.146.95:843','http://120.197.234.166:80','http://120.198.243.113:80','http://120.198.243.114:80','http://120.198.243.116:80','http://120.198.243.118:80','http://120.198.243.130:80','http://120.198.243.14:80','http://120.198.243.151:80','http://120.198.243.15:80','http://120.198.243.3:80','http://120.198.243.50:80','http://120.198.243.51:80','http://120.198.243.52:80','http://120.198.243.53:80','http://120.198.243.54:80','http://120.198.243.82:80','http://120.198.243.83:80','http://120.198.243.86:80','http://120.236.148.113:3128','http://121.201.18.74:3128','http://121.243.51.107:80','http://121.243.51.107:8080','http://122.225.106.35:80','http://122.96.59.106:80','http://122.96.59.106:82','http://122.96.59.106:83','http://122.96.59.106:843','http://123.110.75.213:9064','http://123.125.104.242:80','http://123.125.19.44:80','http://123.138.184.228:80','http://123.155.155.53:80','http://123.205.32.82:8088','http://124.88.67.13:83','http://124.88.67.13:843','http://125.162.214.244:80','http://125.39.66.68:80','http://128.199.113.225:8080','http://162.208.49.45:8089','http://175.43.20.95:80','http://177.84.241.107:3128','http://180.153.100.242:80','http://180.153.100.242:81','http://180.153.100.242:83','http://180.153.100.242:84','http://180.153.100.242:85','http://180.153.100.242:86','http://180.177.182.242:9064','http://182.118.23.7:8081','http://182.118.31.110:80','http://182.235.184.16:8088','http://182.239.127.136:80','http://182.239.127.137:80','http://182.239.127.139:80','http://182.239.127.139:81','http://182.239.127.139:82','http://182.239.127.140:80','http://182.239.127.140:81','http://182.239.127.140:82','http://182.239.95.134:80','http://182.239.95.136:80','http://182.239.95.137:80','http://182.239.95.139:80','http://182.93.83.101:80','http://183.207.224.12:80','http://183.207.224.13:80','http://183.207.224.14:80','http://183.207.224.42:80','http://183.207.224.43:80','http://183.207.224.44:80','http://183.207.224.45:80','http://183.207.224.50:80','http://183.207.224.50:81','http://183.207.224.50:82','http://183.207.224.50:83','http://183.207.224.50:84','http://183.207.224.50:85','http://183.207.224.50:86','http://183.207.224.51:80','http://183.207.224.51:81','http://183.207.224.51:82','http://183.207.224.51:83','http://183.207.224.51:84','http://183.207.224.51:85','http://183.207.224.51:86','http://183.207.224.52:80','http://183.207.224.52:81','http://183.207.224.52:82','http://183.207.224.52:83','http://183.207.224.52:85','http://183.207.224.52:86','http://183.207.228.114:80','http://183.207.228.115:80','http://183.207.228.116:80','http://183.207.228.119:80','http://183.207.228.122:80','http://183.207.228.123:80','http://183.207.228.22:80','http://183.207.228.22:81','http://183.207.228.22:82','http://183.207.228.22:83','http://183.207.228.22:84','http://183.207.228.22:85','http://183.207.228.22:86','http://183.207.228.41:80','http://183.207.228.42:80','http://183.207.228.43:80','http://183.207.228.44:80','http://183.207.228.50:80','http://183.207.228.50:81','http://183.207.228.50:82','http://183.207.228.50:83','http://183.207.228.50:84','http://183.207.228.50:85','http://183.207.228.51:80','http://183.207.228.51:81','http://183.207.228.51:82','http://183.207.228.51:83','http://183.207.228.51:85','http://183.207.228.52:80','http://183.207.228.52:81','http://183.207.228.52:83','http://183.207.228.52:84','http://183.207.228.52:85','http://183.207.228.52:86','http://183.207.228.54:80','http://183.207.228.54:82','http://183.207.228.54:83','http://183.207.228.54:84','http://183.207.228.54:85','http://183.207.228.54:86','http://183.207.228.56:80','http://183.207.228.57:80','http://183.207.228.58:80','http://183.207.228.60:80','http://183.207.229.130:81','http://183.207.229.130:82','http://183.207.229.130:83','http://183.207.229.130:85','http://183.207.229.137:6969','http://183.207.229.137:7070','http://183.207.229.137:8000','http://183.207.229.137:8001','http://183.207.229.137:8080','http://183.207.229.137:8088','http://183.207.229.137:8089','http://183.207.229.137:88','http://183.207.229.137:8888','http://183.207.229.137:9001','http://183.207.229.137:9090','http://183.207.229.137:9999','http://183.207.229.138:6969','http://183.207.229.138:7070','http://183.207.229.138:8000','http://183.207.229.138:8001','http://183.207.229.138:8080','http://183.207.229.138:8086','http://183.207.229.138:8088','http://183.207.229.138:8089','http://183.207.229.138:8090','http://183.207.229.138:9001','http://183.207.229.138:9090','http://183.207.229.138:9999','http://183.207.229.139:80','http://183.207.229.139:8088','http://183.207.229.139:8090','http://183.207.229.139:88','http://183.207.229.15:80','http://183.207.229.17:80','http://183.207.229.17:9000','http://183.207.229.19:80','http://183.207.229.19:8081','http://183.207.229.19:81','http://183.207.229.19:82','http://183.207.229.19:9090','http://183.207.237.11:80','http://183.207.237.11:81','http://183.222.251.247:8123','http://183.224.1.30:80','http://183.228.235.184:8088','http://187.160.240.140:3128','http://188.166.17.183:8080','http://190.167.243.11:8080','http://195.114.125.81:8080','http://199.200.120.37:7808','http://200.178.118.82:3128','http://200.178.118.82:80','http://202.114.144.15:8088','http://202.119.25.227:9999','http://202.119.25.228:9999','http://202.119.25.69:9999','http://202.119.25.70:9999','http://202.119.25.71:9999','http://202.119.25.72:9999','http://202.119.25.73:9999','http://202.138.233.145:8080','http://202.171.253.74:86','http://202.29.235.130:3129','http://202.77.115.71:54321','http://202.77.119.114:3128','http://202.99.16.28:3128','http://203.151.21.184:3128','http://203.172.209.222:8080','http://203.176.140.226:8080','http://209.177.93.6:80','http://210.101.131.231:8080','http://210.101.131.232:8080','http://211.162.0.170:80','http://218.203.54.31:80','http://218.204.141.204:8118','http://218.207.195.206:80','http://218.207.195.206:8000','http://218.207.195.206:8080','http://218.23.27.18:9797','http://218.59.144.120:80','http://218.59.144.120:81','http://218.59.144.95:80','http://218.59.144.95:81','http://219.143.238.174:8080','http://219.223.189.204:3128','http://219.246.90.162:3128','http://219.68.233.62:9064','http://219.93.183.106:8080','http://221.10.102.203:80','http://221.10.102.203:81','http://221.10.102.203:82','http://221.10.102.203:83','http://221.12.173.130:3128','http://221.176.14.72:80','http://221.181.73.45:80','http://221.193.249.140:3128','http://222.33.41.228:80','http://222.35.185.129:8080','http://222.39.87.140:8118','http://222.73.233.134:80','http://222.73.233.135:80','http://222.73.233.136:80','http://222.87.129.218:80','http://222.87.129.218:81','http://222.87.129.218:843','http://223.83.131.168:8123','http://223.85.17.157:8123','http://223.85.22.54:8123','http://223.86.211.80:8123','http://27.200.89.238:9797','http://36.250.74.87:80','http://36.250.74.87:8102','http://36.250.74.87:8103','http://36.250.74.88:80','http://36.250.74.88:8102','http://36.250.74.88:8103','http://36.73.186.106:80','http://42.236.33.176:80','http://42.236.33.177:80','http://42.236.33.178:80','http://42.236.33.179:80','http://42.236.33.180:80','http://46.137.170.174:443','http://46.173.169.48:3128','http://49.1.245.234:3128','http://49.1.245.237:3128','http://5.56.61.26:10241','http://5.56.61.26:12206','http://5.56.61.26:15322','http://58.246.199.122:3128','http://58.251.78.71:8088','http://58.252.167.103:80','http://58.252.72.179:3128','http://60.13.74.183:843','http://60.18.147.42:80','http://60.5.252.76:80','http://61.133.116.37:3128','http://61.156.3.166:80','http://61.156.35.2:3128','http://61.158.173.188:9797','http://61.158.173.188:9999','http://61.162.223.41:9797','http://61.163.165.250:9797','http://61.184.192.42:80','http://61.232.6.164:8081','http://61.53.143.179:80','http://61.54.221.200:3128','http://61.7.147.83:8080','http://61.7.213.58:3128','http://66.35.68.145:3127','http://66.35.68.145:7808','http://66.35.68.145:8089','http://69.164.213.244:3128','http://69.197.148.18:3127','http://69.197.148.18:7808','http://69.197.148.18:8089','http://78.189.30.243:8080','http://78.24.221.193:3128','http://79.142.57.118:3128','http://81.163.88.65:8080','http://83.55.33.54:8080','http://86.107.110.73:3127','http://86.107.110.73:7808','http://87.120.58.129:8080','http://88.132.82.236:8088','http://88.150.136.179:3129','http://88.150.136.180:3129','http://89.249.207.65:3128','http://91.215.108.131:3130','http://94.23.23.60:80']

PROXY = proxy_change(proxy_list)
crawling_module.write_text_to_file_by_utf8('logger.csv', '現在使用してるプロキシは'+PROXY , 1)
ACCESS_COUNT = 0

start_list = [1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000, 11000000, 12000000, 13000000, 14000000, 15000000, 16000000, 17000000, 18000000, 19000000, 20000000, 21000000, 22000000, 23000000, 24000000, 25000000, 26000000, 27000000, 28000000, 29000000, 30000000, 31000000, 32000000, 33000000, 34000000, 35000000, 36000000, 37000000, 38000000, 39000000, 40000000, 41000000, 42000000, 43000000, 44000000, 45000000, 46000000, 47000000]
ended_list = [1014267, 2008782, 3008230, 4016220, 5006963, 6007865, 7012233, 8016785, 9014790, 10015240, 11038450, 12036105, 13171150, 14057830, 15015390, 16007268, 17009425, 18006588, 19008345, 20018724, 21014785, 22027990, 23055515, 24013130, 25007515, 26025189, 27083790, 28042900, 29009190, 30007300, 31004139, 32004525, 33012580, 34020420, 35008830, 36005615, 37008170, 38010535, 39005485, 40038899, 41005425, 42009014, 43011110, 44008400, 45007345, 46010215, 47015263]

#####開始県域を設定
i = 0

while i <= len(start_list)-1:  ####エンド県域を設定

    for k in range(start_list[i], ended_list[i], 1):
        #######プロキシの変更が必要かどうかを判断
        if ACCESS_COUNT > MAX_NUMBER:
            PROXY = proxy_change(proxy_list)
            crawling_module.write_text_to_file_by_utf8('logger.csv', '現在使用してるプロキシは'+PROXY,1)
            ACCESS_COUNT = 0

        #######データを取得し、ファイルに書き込み
        if PROXY is not None:
            shop_url ='http://tabelog.com/tokyo/A1307/A130701/' + str(k)
            write_data_to_file_by_url(shop_url, PROXY)
            ACCESS_COUNT += 1

    i += 1

