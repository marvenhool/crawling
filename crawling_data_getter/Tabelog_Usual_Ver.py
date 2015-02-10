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
proxy_list = ['http://1.34.220.170:8088','http://101.227.252.130:8081','http://101.4.136.34:9999',
              'http://101.71.27.27:8000','http://110.4.12.173:80','http://110.78.155.132:80',
              'http://111.1.36.133:80','http://111.1.36.6:80','http://111.1.61.23:8080','http://111.12.128.166:80',
              'http://112.170.72.132:3128','http://113.105.224.87:80','http://113.207.128.129:80',
              'http://113.207.129.129:80','http://114.34.148.204:3128','http://117.135.194.53:80',
              'http://117.135.250.51:80','http://117.135.250.51:82','http://117.135.250.51:86','http://117.135.250.53:80',
              'http://117.135.250.54:80','http://117.135.250.54:84','http://117.135.250.55:80','http://117.135.250.56:80',
              'http://117.135.250.68:80','http://117.135.250.83:80','http://117.135.250.84:80','http://117.135.250.86:80',
              'http://117.135.250.9:80','http://117.135.251.74:82','http://117.135.251.76:82','http://117.135.251.78:80',
              'http://117.135.252.14:80','http://117.135.252.14:82','http://117.135.252.14:84','http://117.149.213.212:8123',
              'http://117.177.243.79:80','http://119.40.98.26:8080','http://120.126.50.118:9064','http://120.131.128.209:80',
              'http://120.193.146.95:843','http://120.197.234.166:80','http://120.198.243.131:80','http://120.202.249.230:80',
              'http://121.243.51.107:80','http://121.42.138.65:3128','http://123.110.121.135:8088','http://123.125.19.44:80',
              'http://123.138.185.50:80','http://123.194.41.185:8088','http://123.195.131.10:8088','http://123.195.192.152:9064',
              'http://124.11.129.123:8088','http://124.88.67.13:83','http://142.54.170.72:3127','http://142.54.170.72:7808',
              'http://159.8.36.242:3128','http://162.208.49.45:8089','http://175.43.20.95:80','http://177.69.195.4:3128',
              'http://180.248.17.135:3128','http://182.239.127.134:80','http://183.207.224.50:80','http://183.207.224.50:81',
              'http://183.207.224.50:82','http://183.207.224.50:85','http://183.207.224.51:80','http://183.207.224.51:83',
              'http://183.207.224.51:84','http://183.207.224.52:80','http://183.207.224.52:81','http://183.207.228.115:80',
              'http://183.207.228.122:80','http://183.207.228.123:80','http://183.207.228.22:80','http://183.207.228.22:82',
              'http://183.207.228.22:84','http://183.207.228.22:85','http://183.207.228.22:86','http://183.207.228.23:80',
              'http://183.207.228.23:81','http://183.207.228.23:85','http://183.207.228.23:86','http://183.207.228.42:80',
              'http://183.207.228.44:80','http://183.207.228.50:80','http://183.207.228.50:81','http://183.207.228.50:82',
              'http://183.207.228.50:83','http://183.207.228.50:84','http://183.207.228.51:80','http://183.207.228.51:82',
              'http://183.207.228.51:83','http://183.207.228.52:80','http://183.207.228.52:83','http://183.207.228.52:84',
              'http://183.207.228.52:85','http://183.207.228.54:80','http://183.207.228.57:80','http://183.207.228.58:80',
              'http://183.207.229.15:80','http://183.224.1.30:80','http://185.72.156.19:3127','http://199.200.120.37:7808',
              'http://200.90.106.52:9064','http://202.106.16.36:3128','http://202.119.25.69:9999','http://202.171.253.74:86',
              'http://203.151.21.184:3128','http://203.192.10.66:80','http://212.112.124.137:8080','http://217.21.43.237:3128',
              'http://218.65.132.45:8081','http://219.246.90.162:3128','http://219.93.183.106:8080','http://222.171.28.121:3128',
              'http://222.87.129.218:843','http://223.83.211.203:8123','http://31.25.142.216:3128','http://36.250.74.88:8103',
              'http://41.205.231.202:8080','http://41.216.159.158:8080','http://58.242.249.14:33942','http://58.242.249.52:17657',
              'http://58.251.78.71:8088','http://58.99.120.122:8088','http://60.244.66.86:8088','http://60.55.49.9:3128',
              'http://61.54.221.200:3128','http://61.70.110.151:8088','http://69.197.148.18:3127','http://69.197.148.18:7808',
              'http://69.197.148.18:8089','http://80.63.55.3:8080','http://83.241.46.175:8080','http://86.107.110.73:3127',
              'http://88.132.82.236:8088','http://91.121.108.174:3128']


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