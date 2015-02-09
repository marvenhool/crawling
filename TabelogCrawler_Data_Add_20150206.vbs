Option Explicit

Dim Http
Dim buf
Dim buf2
Set Http = CreateObject("MSXML2.XMLHTTP")
Dim TitleStart
Dim TitleEnd
Dim Title

Dim jnlStart
Dim jnlEnd
Dim jnl

'''' 電話番号 ''''
Dim tel
Dim ipp

Dim TscrStart
Dim TscrEnd
Dim Tscr

Dim DscrStart
Dim DscrEnd
Dim Dscr

Dim LscrStart
Dim LscrEnd
Dim Lscr

'''' 予約可否変数 ''''
Dim ResStart
Dim ResEnd
Dim Res


''''''ネット予約可否
Dim netBooking

'''''''''''''''

'''''''口コミ数'''
Dim comment 


'''' 住所変数 ''''
Dim AddStart
Dim AddEnd
Dim Add

'''' 住所1変数 ''''
Dim AddStart1
Dim AddEnd1
Dim Add1

'''' GeoCode変数 ''''
Dim GeoStart
Dim GeoEnd
Dim Geo

'''' 営業時間変数 ''''
Dim OpnStart
Dim OpnEnd
Dim Opn

'''' 平均予算昼変数 ''''
Dim YsnDStart
Dim YsnDEnd
Dim YsnD

'''' 平均予算夜変数 ''''
Dim YsnNStart
Dim YsnNEnd
Dim YsnN

'''' 席数 ''''
Dim CheStart
Dim CheEnd
Dim Che

'''' クーポン ''''
Dim CouStart
Dim CouEnd
Dim Cou

'''' 定休日 ''''
Dim HolStart
Dim HolEnd
Dim Hol


'''' 店舗名カナ ''''
Dim KanaStart
Dim KanaEnd
Dim Kana

'''' クレカ ''''
Dim crcStart
Dim crcEnd
Dim crc

'''' 最寄駅 ''''
Dim staStart
Dim staEnd
Dim sta


'''' 閉店チェック ''''
Dim cls

'''' 会員状況確認 ''''
Dim memStart
Dim memEnd
Dim mem

Dim count
Dim YsnBuf

Dim CouBufStart
Dim CouBufEnd
Dim CouBuf

''''アクセス数変数''''
Dim PVtotal
Dim PVlastweek
Dim PVlastweekbefore

''''最終結果用変数''''
Dim Ans


Dim fileNo

Dim errCnt
Dim i

Dim objFSO      ' FileSystemObject
Dim objFile     ' ファイル書き込み用
Set objFSO = WScript.CreateObject("Scripting.FileSystemObject")

''''ファイルパス指定用''''
Dim MyPath
Dim MyFol

MyPath = WScript.ScriptFullName
MyFol  = objFSO.GetParentFolderName(MyPath)



Set objFile = objFSO.OpenTextFile(MyFol & "\漏れた店舗再取得.csv", 8, True, -1)		'4番目の引数は必要。なぜなら、Unicodeで保存しないとエラーが起こる場合がある。

Dim titleString
titleString    =  """店名"","&"""口コミ数"","&"""カナ"","&"""CENAネット予約可否"","&"""閉店チェック"","&"""会員状況確認"","&"""ジャンル"","&"""電話"","&"""IP電話"","&"""アクセス"","&"""総スコア"","&"""夜スコア"","&"""昼スコア"","&"""予約可否"","&"""住所"","&"""経緯度"","&"""営業時間"","&"""平均予算昼"","&"""平均予算夜"","&"""席数"","&"""クーポン"","&"""定休日"","&"""カード"","&"""URL"","&"""総PV数"","&"""先週PV数"","&"""先々週PV数"","&"""プレミアムクーポン有無"","&"""県域コード"","&"""公式情報あり"""        
objFile.WriteLine(titleString)

Dim temArrar
temArrar = Array("2004551","2004772","2004778","2004787","2004791","2004800","2004803","2004816","2004856","2004899","2004915","2004924","2005000","2005004","2005005","2005006","2005007","2005013","2005024","2005026","2005030","2005031","2005033","2005039","2005050","2005055","2005058","2005059","2005062","2005065","2005066","2005077","2005080","2005082","2005083","2005085","2005086","2005088","2005096","2005097","2005098","2005115","2005127","2005136","2005145","2005187","2005191","2005243","2005293","2005304","2005308","2005311","2005363","2005364","2005365","2005366","2005367","2005368","2005369","2005370","2005371","2005372","2005373","2005374","2005375","2005376","2005377","2005378","2005379","2005381","2005385","2005390","2005391","2005392","2005481","2005622","2005627","2005659","2005661","2005662","2005665","2005666","2005669","2005672","2005673","2005674","2005676","2005677","2005678","2005682","2005684","2005688","2005690","2005691","2005693","2005696","2005697","2005756","2005782","2005783","2005784","2005785","2005786","2005787","2005788","2005789","2005790","2005791","2005792","2005793","2005794","2005795","2005829","2005830","2005833","2005854","2005860","2005898","2005899","2005922","2005931","2005941","2005962","2006054","2006099","2006100","2006110","2006185","2006187","2006189","2006226","2006245","2006297","2006316","2006331","2006337","2006342","2006372","2006388","2006402","2006458","2006476","2006519","2006601","2006647","2006709","2006717","2006787","2006814","2006889","2006903","2006908","2006912","2006928","2006939","2006941","2006942","2006943","2006947","2006948","2006949","2006952","2006953")





For i = 0 To UBound(temArrar) Step 1
    
    On Error Resume Next
    
    Http.Open "GET", "http://tabelog.com/hokkaido/A0101/A010101/" & temArrar(i), False
    Http.Send
    
    If Err.Number <> 0 Then 
        Call WriteTextFile(MyFol & "\エラー発生日時.txt", "http://tabelog.com/hokkaido/A0101/A010101/" & i, 1) 
        i = i - 1
        Call WriteTextFile(MyFol & "\エラー発生日時.txt", "次からリスタート：" & i, 1) 
        WScript.sleep(1500000)
    End If
    
    On Error Goto 0
    
    buf = Http.Responsetext
    
    
    '''' 店舗名取得 ''''''''''
    TitleStart = InStr(buf, "<p class=""mname""><strong>") + 25
    TitleEnd = InStr(TitleStart,buf, vbLf) + 1
    If TitleStart > 25 Then
        
        Title = Mid(buf, TitleStart, TitleEnd - TitleStart)
        Title = Replace(Title, "</strong>", "")
        Title = Replace(Title, "</p>", "")
        Title = Replace(Title, vbLf, "")
        Title = Replace(Title, " ", "")
        
        '''' 閉店チェック ''''
        cls = InStr(buf, "<p class=""rst-status-closed"">")
        If cls = 0 Then
            
            cls = "営業中"
            
        Else
            
            cls = "閉店"
            
        End If
        
        '''' ジャンル取得 ''''''''''
        jnlStart = InStr(buf, "<p><span property=""v:category"">") + 31
        jnlEnd = InStr(jnlStart,buf, vbLf) + 1
        
        jnl = Mid(buf, jnlStart, jnlEnd - jnlStart)
        jnl = Replace(jnl, "<span property=""v:category"">", "")
        jnl = Replace(jnl, "</span>", "")
        jnl = Replace(jnl, "</p>", "")
        jnl = Replace(jnl, vbLf, "")
        jnl = Replace(jnl, " ", "")
        
        
        '''' 電話取得 ''''''''''
        If cls = "閉店" Then
            tel = ""
        Else
            
            tel = fsGetWordsBetween(buf, "<p class=""ppc-sub"">", "</strong>")
            tel = Replace(tel, "<strong>", "")
            tel = Replace(tel, vbLf, "")
            tel = Replace(tel, vbCr, "")
            tel = Replace(tel, " ", "")
            tel = Replace(tel, "	", "")
            
            ipp = fsGetWordsBetween(buf, "<strong property=""v:tel"">", "</strong>")
            ipp = Replace(ipp, "<strong>", "")
            ipp = Replace(ipp, vbLf, "")
            ipp = Replace(ipp, vbCr, "")
            ipp = Replace(ipp, " ", "")
            ipp = Replace(ipp, "	", "")
            
            If tel = "" Then
            tel = ipp
            ipp = ""
            End if
            
        End If 
        
        
        '''' 総スコア取得 ''''''''''
        TscrStart = InStr(buf, "<strong class=""score"" rel=""v:rating""><span property=""v:average"">") + 64
        TscrEnd = InStr(TscrStart,buf, vbLf) + 1
        Tscr = Mid(buf, TscrStart, TscrEnd - TscrStart)
        Tscr = Replace(Tscr, "</span>", "")
        Tscr = Replace(Tscr, "</strong>", "")
        Tscr = Replace(Tscr, vbLf, "")
        Tscr = Replace(Tscr, " ", "")
        
        '''' 夜スコア取得 ''''''''''
        DscrStart = InStr(buf, "<span class=""dinner"">夜の点数：</span><em>") + 37
        DscrEnd = InStr(DscrStart,buf, vbLf) + 1
        Dscr = Mid(buf, DscrStart, DscrEnd - DscrStart)
        Dscr = Replace(Dscr, "</em>", "")
        Dscr = Replace(Dscr, vbLf, "")
        Dscr = Replace(Dscr, " ", "")
        
        '''' 昼スコア取得 ''''''''''
        LscrStart = InStr(buf, "<span class=""lunch"">昼の点数：</span><em>") + 36
        LscrEnd = InStr(LscrStart,buf, vbLf) + 1
        Lscr = Mid(buf, LscrStart, LscrEnd - LscrStart)
        Lscr = Replace(Lscr, "</em>", "")
        Lscr = Replace(Lscr, vbLf, "")
        Lscr = Replace(Lscr, " ", "")
        
        '↓↓初田付け足し
        
        '''' アクセス総数取得 ''''''
        PVtotal = fsGetWordsBetween(buf, "アクセス数 <em>", "</em>")
        
        '''' 先週のアクセス数取得 ''''''
        PVlastweek = fsGetWordsBetween(buf, "先週のアクセス数：</span><em>", "</em>")
        
        '''' 先々週のアクセス数取得 ''''''
        PVlastweekbefore = fsGetWordsBetween(buf, "先々週のアクセス数：</span><em>", "</em>")
        
        '↑↑初田付け足し
        
        '''' 平均予算 ''''
        
        YsnN = ""
        YsnD = ""
        
        YsnBuf = fsGetWordsBetween(buf, "<th>予算", "</td>")
        
        YsnN = fsGetWordsBetween(YsnBuf, "[夜]</span><span class=""price"">", "</span>")
        YsnN = Replace(YsnN, "（", "")
        YsnN = Replace(YsnN, "）", "")
        YsnN = Replace(YsnN, vbLf, "")
        YsnN = Replace(YsnN, vbCr, "")
        YsnN = Replace(YsnN, " ", "")
        YsnN = Replace(YsnN, "	", "")
        
        If YsnN = "" Then 
            
            YsnN = fsGetWordsBetween(YsnBuf, "<dt class=""budget-dinner"">夜の予算</dt>", "</dd>")
            YsnN = fsGetWordsBetween(YsnN, "class=""num""", "</dd>")
            YsnN = Replace(YsnN, "</a>", "")
            YsnN = Replace(YsnN, "property=""v:pricerange"">", "")
            YsnN = Replace(YsnN, "</em>", "")
            YsnN = Replace(YsnN, vbLf, "")
            YsnN = Replace(YsnN, vbCr, "")
            YsnN = Replace(YsnN, " ", "")
            YsnN = Replace(YsnN, "	", "")
            
        End If 
        
        
        YsnD = fsGetWordsBetween(YsnBuf, "[昼]</span><span class=""price"">", "</span>")
        YsnD = Replace(YsnD, "（", "")
        YsnD = Replace(YsnD, "）", "")
        YsnD = Replace(YsnD, vbLf, "")
        YsnD = Replace(YsnD, vbCr, "")
        YsnD = Replace(YsnD, " ", "")
        YsnD = Replace(YsnD, "	", "")
        
        If YsnD = "" Then 
            
            YsnD = fsGetWordsBetween(YsnBuf, "<dt class=""budget-lunch"">昼の予算</dt>", "</dd>")
            YsnD = fsGetWordsBetween(YsnD, "class=""num""", "</dd>")
            YsnD = Replace(YsnD, "</a>", "")
            YsnD = Replace(YsnD, ">", "")
            YsnD = Replace(YsnD, "</em>", "")
            YsnD = Replace(YsnD, vbLf, "")
            YsnD = Replace(YsnD, vbCr, "")
            YsnD = Replace(YsnD, " ", "")
            YsnD = Replace(YsnD, "	", "")
            
        End If 
        
        '''' 営業時間変数 ''''
        OpnStart = InStr(buf, "<th>営業時間</th>") + 13
        OpnEnd = InStr(OpnStart,buf, vbLf) + 1
        OpnEnd = InStr(OpnEnd,buf, "</td>")
        Opn = Mid(buf, OpnStart, OpnEnd - OpnStart)
        
        Opn = Replace(Opn, "<tr>", "")
        Opn = Replace(Opn, "</tr>", "")
        Opn = Replace(Opn, "<td>", "")
        Opn = Replace(Opn, "</td>", "")
        Opn = Replace(Opn, "<p>", "")
        Opn = Replace(Opn, "</p>", "")
        
        Opn = Replace(Opn, "<br />", vbLf)
        
        Opn = Replace(Opn, vbLf, "")
        Opn = Replace(Opn, " ", "")
        
        
        '''' 定休日 ''''
        HolStart = InStr(buf, "<th>定休日</th>") + 12
        HolEnd = InStr(HolStart,buf, vbLf) + 1
        HolEnd = InStr(HolEnd,buf, vbLf)
        Hol = Mid(buf, HolStart, HolEnd - HolStart)
        
        Hol = Replace(Hol, "<td>", "")
        Hol = Replace(Hol, "</td>", "")
        Hol = Replace(Hol, "<p>", "")
        Hol = Replace(Hol, "</p>", "")
        Hol = Replace(Hol, vbLf, "")
        Hol = Replace(Hol, " ", "")
        
        
        '''' 席数 ''''
        CheStart = InStr(buf, "<th>席数</th>") + 11
        
        If CheStart > 11 Then
            
            CheEnd = InStr(CheStart,buf, vbLf)
            CheEnd = InStr(CheEnd,buf, vbLf) + 1
            CheEnd = InStr(CheEnd,buf, vbLf) + 1
            CheEnd = InStr(CheEnd,buf, vbLf) + 1
            CheEnd = InStr(CheEnd,buf, vbLf) + 1
            
            Che = Mid(buf, CheStart, CheEnd - CheStart)
            
            Che = Replace(Che, "<td>", "")
            Che = Replace(Che, "</td>", "")
            Che = Replace(Che, "<p>", "")
            Che = Replace(Che, "</p>", "")
            Che = Replace(Che, "</tr>", "")
            Che = Replace(Che, "<strong>", "")
            Che = Replace(Che, "</strong>", "")
            
            Che = Replace(Che, vbLf, "")
            Che = Replace(Che, " ", "")
            
        Else
            
            ' 席数記載なし
            Che = ""
            
        End If
        
        
        '''' クレカ ''''
        crcStart = InStr(buf, "<th>カード</th>") + 12
        
        If crcStart > 12 Then
            
            crcEnd = InStr(crcStart,buf, vbLf)
            crcEnd = InStr(crcEnd,buf, vbLf) + 1
            crcEnd = InStr(crcEnd,buf, vbLf) + 1
            
            crc = Mid(buf, crcStart, crcEnd - crcStart)
            
            crc = Replace(crc, "<td>", "")
            crc = Replace(crc, "</td>", "")
            crc = Replace(crc, "<p>", "")
            crc = Replace(crc, "</p>", "")
            crc = Replace(crc, "<strong>", "")
            crc = Replace(crc, "</strong>", "")
            
            crc = Replace(crc, vbLf, "")
            crc = Replace(crc, " ", "")
            
        Else
            
            ' クレカ記載なし
            crc = ""
            
        End If
        
        '''' 最寄駅 ''''
        staStart = InStr(buf, "<th>交通手段</th>") + 13
        
        If staStart > 13 Then
            
            staEnd = InStr(staStart,buf, vbLf)
            staEnd = InStr(staEnd,buf, "</td>")
            
            sta = Mid(buf, staStart, staEnd - staStart)
            
            sta = Replace(sta, "<td>", "")
            sta = Replace(sta, "</td>", "")
            sta = Replace(sta, "<p>", "")
            sta = Replace(sta, "</p>", "")
            sta = Replace(sta, "<br/>", " ")
            sta = Replace(sta, vbLf, "")
            sta = Replace(sta, " ", "")
            
        Else
            
            ' 最寄駅記載なし
            sta = ""
            
        End If
        
        '''' クーポン ''''
        Cou = ""
        CouBufStart = InStr(buf, "<div class=""rstinfo-coupon"">") + 28
        
        If CouBufStart > 28 Then
            
            CouBufEnd = InStr(buf, "<div id=""rstinfo-actions"">")
            CouBuf = Mid(buf, CouBufStart, CouBufEnd - CouBufStart)
            
            ' 無駄なスクリプトの削除
            Do Until InStr(CouBuf, "//<![CDATA[") = 0
                
                CouBufStart = InStr(CouBuf, "//<![CDATA[")
                CouBufEnd = InStr(CouBuf, "//]]>") + 5
                
                CouBuf = Replace(CouBuf,Mid(CouBuf, CouBufStart, CouBufEnd - CouBufStart),"")
                
            Loop
            
            ' 印刷XMLを削除
            Do Until InStr(CouBuf, "このクーポンを印刷</a>") = 0
                
                CouBufStart = InStr(CouBuf, "このクーポンを印刷</a>")
                
                CouBufStart = InStrRev(CouBuf, vbLf,CouBufStart)
                
                CouBufEnd = InStr(CouBufStart,CouBuf, "</li>") + 5
                
                CouBuf = Replace(CouBuf,Mid(CouBuf, CouBufStart, CouBufEnd - CouBufStart),"")
                
            Loop
            
            CouBuf = Replace(CouBuf, "<ul class=""coupon-list clearfix"">", "")
            CouBuf = Replace(CouBuf, "<p class=""coupon-bg"">", "")
            CouBuf = Replace(CouBuf, "</ul>", "")
            CouBuf = Replace(CouBuf, "</div>", "")
            CouBuf = Replace(CouBuf, "<script type=""text/javascript"">", "")
            CouBuf = Replace(CouBuf, "</script>", "")
            CouBuf = Replace(CouBuf, "<li class=""tabelog-coupon"">", "")
            CouBuf = Replace(CouBuf, "<li class=""other-coupon"">", "")
            
            ' 最終加工
            Do Until InStr(CouBuf, "<span class=""title"">") = 0
                
                CouBufStart = InStr(CouBuf, "<span class=""title"">")
                
                CouBufEnd = InStr(CouBufStart,CouBuf, "</span>") + 7
                
                Cou = Cou & Mid(CouBuf, CouBufStart, CouBufEnd - CouBufStart) & vbLf
                
                CouBuf = Replace(CouBuf,Mid(CouBuf, CouBufStart, CouBufEnd - CouBufStart),"")
                
            Loop
            
            Cou = Replace(Cou, "<span class=""ex"">", "")
            Cou = Replace(Cou, "<span class=""title"">", "")
            Cou = Replace(Cou, "</span>", "")
            Cou = Replace(Cou, " ", "")
            Cou = Left(Cou,Len(Cou)-1)
            
            
            
        Else
            
            Cou = "クーポン情報なし"
            
        End If
        
        
        '''' 予約可否変数 ''''
        ResStart = InStr(buf, "予約可")
        
        If ResStart = 0 Then
            
            ResStart = InStr(buf, "予約不可")
            
            If ResStart = 0 Then
                
                Res = ""
                
            Else
                
                Res = "予約不可"
                
            End If
            
        Else
            
            Res = "予約可"
            
        End If
        
        '''' 住所変数 ''''
        AddStart = InStr(buf, "<th>住所</th>") + 11
        
        If AddStart > 11 Then
            
            AddEnd = InStr(buf, "<div class=""map-morelinks clearfix"">")
            
            If AddEnd <> 0 Then
                
                ' 住所情報＋ジオコード
                Add = Mid(buf, AddStart, AddEnd - AddStart)
                
                AddStart1 = InStr(Add, "<span property=""v:region"">") + 26
                AddEnd1 = InStr(Add, "<div class=""rst-map-wrap"">")
                Add1 = Mid(Add, AddStart1, AddEnd1 - AddStart1)
                
                Add1 = Replace(Add1, "</a>", "")
                Add1 = Replace(Add1, "</span>", "")
                Add1 = Replace(Add1, "</p>", "")
                Add1 = Replace(Add1, "<span property=""v:locality"">", "")
                Add1 = Replace(Add1, "<span property=""v:street-address"">", "")
                
                ' 最初のタグを消す
                AddEnd1 = InStr(Add1, ">")
                Add1 = Replace(Add1,Left(Add1,AddEnd1),"")
                
                ' 余計なタグは消す
                Do Until InStr(Add1, "<") = 0
                    AddStart1 = InStr(Add1, "<")
                    AddEnd1 = InStr(Add1, ">") + 1
                    Add1 = Replace(Add1,Mid(Add1,AddStart1,AddEnd1 - AddStart1), " ")
                    
                Loop
                
                Add1 = Replace(Add1, vbLf, "")
                Add1 = Replace(Add1, " ", "")
                Add1 = Replace(Add1, "　", "")
                
                ' ジオコード
                GeoStart = InStr(Add, "center=") + 7
                GeoEnd = InStr(Add, "&amp;markers=")
                
                Geo = Mid(Add, GeoStart, GeoEnd - GeoStart)
                
            Else
                
                ' 地図詳細なし
                Add1 = ""
                Geo = ""
                
            End If
            
        Else
            
            ' 地図情報なし
            Add1 = ""
            Geo = ""
            
        End If
        
        '''' 店舗名カナがある場合は取得 ''''
        If InStr(Title, "（") > 0 Then
            
            KanaStart = InStr(Title, "（") + 1
            KanaEnd = InStr(Title, "）") 
            
            If KanaStart <> 0 And KanaEnd <> 0 And KanaStart < KanaEnd Then
                
                Kana = Mid(Title, KanaStart, KanaEnd - KanaStart)
                
                Title = Mid(Title, 1, KanaStart - 2)
                
            Else
                
                ' 変なデータは諦める
                Kana = ""
                
            End If
            
        Else
            
            ' カナないのは諦める
            Kana = ""
            
        End If
        
        '''' 会員情報を分析 ''''
        memStart = InStr(buf, "このレストランは食べログ店舗会員に登録しているため、ユーザの皆様は編集することができません。") 
        
        If memStart > 0 Then
            
            ' 会員
            memStart = InStr(buf, "<div class=""listing"">") 
            
            If memStart > 0 Then
                
                mem = "無料会員"
                
            Else
                
                mem = "有料会員"
                
            End If
            
        Else
            
            ' 非会員
            mem = "非会員"
            
        End If
        
        
        ''''''''''''口コミ数''''''''''''''''''''''
        
        comment = fsGetWordsBetween(buf, "<em class=""num"" property=""v:count"">", "</em>")
        comment = Replace(comment, "（", "")
        comment = Replace(comment, "）", "")
        comment = Replace(comment, vbLf, "")
        comment = Replace(comment, vbCr, "")
        comment = Replace(comment, " ", "")
        comment = Replace(comment, "	", "")
        
        
        ''''''''''''''''ネット予約可否''''''''''''''''
        
        
        If InStr(buf ,"_side_calendar_widget.js") = 0 Then 
            
            
            netBooking = "ネット予約不可"
            
        Else 
            
            netBooking = "ネット予約可"
            
        End If 
        
        
        ''''''''''''''''preCoupon''''''''''''''''''''''
        Dim preCoupon
        
        
        If InStr(buf ,"<span class=""pcoupon-item-lead"">") <> 0 Then 
            
            preCoupon = "あり"
        Else 
            preCoupon = "なし"
        End If 
        
        
        '''''''''''''''''''''''''''''''''''''''''''''
        ''''''''''''''''kenikicode''''''''''''''''''''''
        
        
        Dim kenikicode
        
        kenikicode = temArrar(i)
        
        If Len(kenikicode) = 7 Then 
            
            kenikicode = Mid(kenikicode, 1, 1)
            
        Else 
            kenikicode = Mid(kenikicode, 1, 2)
            
        End If 
        
        '''''''''''''''''''公式情報あり''''''''''''''''
        Dim offical
        
        If InStr(buf ,"<a class=""official-badge"">公式情報あり</a>") <> 0 Then 
            
            offical = "公式情報あり"
            
        Else 
            
            offical = "公式情報ない"
            
        End If 
        
        
        '''''''''''''''''''''''''''''''''''''''''''''
        
        
        
        '''''''''''''''''''''''''''''''''''''''''''''
        
        Ans    = """" & Title & """,""" & comment& """,""" & Kana & """,""" & netBooking & """,""" & cls & """,""" & mem & """,""" & jnl & """,""" & tel & """,""" & ipp & """,""" & sta & """,""" & Tscr & """,""" & Dscr & """,""" & Lscr & """,""" & Res & """,""" & Add1 & """,""" & Geo & """,""" & Opn & """,""" & YsnD & """,""" & YsnN & """,""" & Che & """,""" & Cou & """,""" & Hol & """,""" & crc & """,""http://tabelog.com/hokkaido/A0101/A010103/" & temArrar(i) & """,""" & PVtotal & """,""" & PVlastweek & """,""" & PVlastweekbefore & ""","""& preCoupon & """,""" & kenikicode& """,""" &offical& """" 
        
        Ans	   = Replace(Ans, vbCrLf, "")
        Ans	   = Replace(Ans, vbCr  , "")
        Ans	   = Replace(Ans, vbLf  , "")
        
        'On Error Resume Next
        
        objFile.WriteLine(Ans)
        
        'If Err.number <> 0 Then
        '	MsgBox(Ans)
        'End If
        
        errCnt = 0
        
    Else
        
        errCnt = errCnt + 1
        
        If errCnt > 99 Then
            
            Dim istr
            
            istr = i
            
            If Len(istr) = 7 Then
                
                istr = Left(istr, 1) & "000000"
                
            Else
                
                istr = Left(istr, 2) & "000000"
                
            End If
            
            i = istr
            
            i = i + 1000000
            
            'MsgBox(i)
            
            Call WriteTextFile(MyFol & "\記録.txt", i, 1 )
            
        End If
        
    End If
    
Next

Set Http = Nothing

objFile.Close                               'ファイルを閉じる

MsgBox "処理が完了しました。"

'-------------------------------------------------------------------------------
' 関　数      Private Function fsGetWordsBetween(ByVal P_sTargetWords As String, ByVal P_sStart As String, ByVal P_sEnd As String) As String
'
' 引　数      P_sTargetWords：対象文字列        P_sStart：開始文字      P_sEnd：終了文字
'
' 戻　値　　　fsGetWordsBetween：引数で囲われている文字列を取得する。（開始文字が見つからなかったときはnullを返して終了）
'
' 説　明      ホームページのURL取得プログラム
'
' 履　歴      2013/08/09        Y.Hatsuda        更新
'--------------------------------------------------------------------------------

Private Function fsGetWordsBetween(ByVal P_sTargetWords, ByVal P_sStart, ByVal P_sEnd)
    
    ''''''''''''''変数''''''''''''''
    
    Dim lngPreWord		'区切り前の文字の文字数
    Dim lngEndWord		'区切り後の文字の文字数
    
    Dim lngStart
    Dim lngEnd
    
    ''''''''''''''''''''''''''''''''
    '囲っている文字の文字数を取得する
    lngPreWord = Len(P_sStart)
    lngEndWord = Len(P_sEnd)
    
    '開始文字列が
    If InStr(P_sTargetWords, P_sStart) = 0 Then 
        
        fsGetWordsBetween = ""
        
    Else 
        
        lngStart = InStr(P_sTargetWords, P_sStart) + lngPreWord
        lngEnd = InStr(lngStart, P_sTargetWords, P_sEnd)
        On Error Resume Next
        fsGetWordsBetween = Mid(P_sTargetWords, lngStart, lngEnd - lngStart)
        On Error Goto 0
        
    End If
    
End Function

'-------------------------------------------------------------------------------
' 関　数      Private Sub WriteTextFile(ByVal P_sFilePath, ByVal P_sWriteWords, ByVal sNeedTime )
'
' 引　数      P_sFilePath：テキストファイルのパス        P_sWriteWords:書出し文言	sNeedTime:時間の書出しが必要な場合は1、それ以外の場合は書き出しを行わない
'
' 戻　値　　　なし
'
' 説　明      テキストファイルへの書き込み。ファイルが存在しない場合は作成して書き込む
'
' 履　歴      2013/08/08        T.Kosaka        新規作成
'--------------------------------------------------------------------------------

Private Sub WriteTextFile(ByVal P_sFilePath, ByVal P_sWriteWords, ByVal sNeedTime )
    
    ''''''''''''''変数''''''''''''''
    
    Dim FSO		'ファイルシステムオブジェクト
    Dim oLog	'テキスト
    Dim Ts		'テキストファイル
    
    ''''''''''''''''''''''''''''''''
    'インスタンスの作成
    Set FSO = CreateObject("Scripting.FileSystemObject")
    
    If FSO.FileExists(P_sFilePath) = False Then
        Set Ts = FSO.CreateTextFile(P_sFilePath)
        Ts.Close
        Set Ts = Nothing
    End If
    
    Set oLog = FSO.GetFile(P_sFilePath)
    Set Ts = oLog.OpenAsTextStream(8)
    
    If sNeedTime = 1 Then
        Ts.WriteLine Now & vbTab & P_sWriteWords
    Else
        Ts.WriteLine P_sWriteWords
    End If
    
    Ts.Close
    Set Ts = Nothing
    Set oLog = Nothing
    Set FSO = Nothing
    
End Sub
