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

'''' �d�b�ԍ� ''''
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

'''' �\��ەϐ� ''''
Dim ResStart
Dim ResEnd
Dim Res


''''''�l�b�g�\���
Dim netBooking

'''''''''''''''

'''''''���R�~��'''
Dim comment 


'''' �Z���ϐ� ''''
Dim AddStart
Dim AddEnd
Dim Add

'''' �Z��1�ϐ� ''''
Dim AddStart1
Dim AddEnd1
Dim Add1

'''' GeoCode�ϐ� ''''
Dim GeoStart
Dim GeoEnd
Dim Geo

'''' �c�Ǝ��ԕϐ� ''''
Dim OpnStart
Dim OpnEnd
Dim Opn

'''' ���ϗ\�Z���ϐ� ''''
Dim YsnDStart
Dim YsnDEnd
Dim YsnD

'''' ���ϗ\�Z��ϐ� ''''
Dim YsnNStart
Dim YsnNEnd
Dim YsnN

'''' �Ȑ� ''''
Dim CheStart
Dim CheEnd
Dim Che

'''' �N�[�|�� ''''
Dim CouStart
Dim CouEnd
Dim Cou

'''' ��x�� ''''
Dim HolStart
Dim HolEnd
Dim Hol


'''' �X�ܖ��J�i ''''
Dim KanaStart
Dim KanaEnd
Dim Kana

'''' �N���J ''''
Dim crcStart
Dim crcEnd
Dim crc

'''' �Ŋ�w ''''
Dim staStart
Dim staEnd
Dim sta


'''' �X�`�F�b�N ''''
Dim cls

'''' ����󋵊m�F ''''
Dim memStart
Dim memEnd
Dim mem

Dim count
Dim YsnBuf

Dim CouBufStart
Dim CouBufEnd
Dim CouBuf

''''�A�N�Z�X���ϐ�''''
Dim PVtotal
Dim PVlastweek
Dim PVlastweekbefore

''''�ŏI���ʗp�ϐ�''''
Dim Ans


Dim fileNo

Dim errCnt
Dim i

Dim objFSO      ' FileSystemObject
Dim objFile     ' �t�@�C���������ݗp
Set objFSO = WScript.CreateObject("Scripting.FileSystemObject")

''''�t�@�C���p�X�w��p''''
Dim MyPath
Dim MyFol

MyPath = WScript.ScriptFullName
MyFol  = objFSO.GetParentFolderName(MyPath)



Set objFile = objFSO.OpenTextFile(MyFol & "\�R�ꂽ�X�܍Ď擾.csv", 8, True, -1)		'4�Ԗڂ̈����͕K�v�B�Ȃ��Ȃ�AUnicode�ŕۑ����Ȃ��ƃG���[���N����ꍇ������B

Dim titleString
titleString    =  """�X��"","&"""���R�~��"","&"""�J�i"","&"""CENA�l�b�g�\���"","&"""�X�`�F�b�N"","&"""����󋵊m�F"","&"""�W������"","&"""�d�b"","&"""IP�d�b"","&"""�A�N�Z�X"","&"""���X�R�A"","&"""��X�R�A"","&"""���X�R�A"","&"""�\���"","&"""�Z��"","&"""�o�ܓx"","&"""�c�Ǝ���"","&"""���ϗ\�Z��"","&"""���ϗ\�Z��"","&"""�Ȑ�"","&"""�N�[�|��"","&"""��x��"","&"""�J�[�h"","&"""URL"","&"""��PV��"","&"""��TPV��"","&"""��X�TPV��"","&"""�v���~�A���N�[�|���L��"","&"""����R�[�h"","&"""������񂠂�"""        
objFile.WriteLine(titleString)

Dim temArrar
temArrar = Array("2004551","2004772","2004778","2004787","2004791","2004800","2004803","2004816","2004856","2004899","2004915","2004924","2005000","2005004","2005005","2005006","2005007","2005013","2005024","2005026","2005030","2005031","2005033","2005039","2005050","2005055","2005058","2005059","2005062","2005065","2005066","2005077","2005080","2005082","2005083","2005085","2005086","2005088","2005096","2005097","2005098","2005115","2005127","2005136","2005145","2005187","2005191","2005243","2005293","2005304","2005308","2005311","2005363","2005364","2005365","2005366","2005367","2005368","2005369","2005370","2005371","2005372","2005373","2005374","2005375","2005376","2005377","2005378","2005379","2005381","2005385","2005390","2005391","2005392","2005481","2005622","2005627","2005659","2005661","2005662","2005665","2005666","2005669","2005672","2005673","2005674","2005676","2005677","2005678","2005682","2005684","2005688","2005690","2005691","2005693","2005696","2005697","2005756","2005782","2005783","2005784","2005785","2005786","2005787","2005788","2005789","2005790","2005791","2005792","2005793","2005794","2005795","2005829","2005830","2005833","2005854","2005860","2005898","2005899","2005922","2005931","2005941","2005962","2006054","2006099","2006100","2006110","2006185","2006187","2006189","2006226","2006245","2006297","2006316","2006331","2006337","2006342","2006372","2006388","2006402","2006458","2006476","2006519","2006601","2006647","2006709","2006717","2006787","2006814","2006889","2006903","2006908","2006912","2006928","2006939","2006941","2006942","2006943","2006947","2006948","2006949","2006952","2006953")





For i = 0 To UBound(temArrar) Step 1
    
    On Error Resume Next
    
    Http.Open "GET", "http://tabelog.com/hokkaido/A0101/A010101/" & temArrar(i), False
    Http.Send
    
    If Err.Number <> 0 Then 
        Call WriteTextFile(MyFol & "\�G���[��������.txt", "http://tabelog.com/hokkaido/A0101/A010101/" & i, 1) 
        i = i - 1
        Call WriteTextFile(MyFol & "\�G���[��������.txt", "�����烊�X�^�[�g�F" & i, 1) 
        WScript.sleep(1500000)
    End If
    
    On Error Goto 0
    
    buf = Http.Responsetext
    
    
    '''' �X�ܖ��擾 ''''''''''
    TitleStart = InStr(buf, "<p class=""mname""><strong>") + 25
    TitleEnd = InStr(TitleStart,buf, vbLf) + 1
    If TitleStart > 25 Then
        
        Title = Mid(buf, TitleStart, TitleEnd - TitleStart)
        Title = Replace(Title, "</strong>", "")
        Title = Replace(Title, "</p>", "")
        Title = Replace(Title, vbLf, "")
        Title = Replace(Title, " ", "")
        
        '''' �X�`�F�b�N ''''
        cls = InStr(buf, "<p class=""rst-status-closed"">")
        If cls = 0 Then
            
            cls = "�c�ƒ�"
            
        Else
            
            cls = "�X"
            
        End If
        
        '''' �W�������擾 ''''''''''
        jnlStart = InStr(buf, "<p><span property=""v:category"">") + 31
        jnlEnd = InStr(jnlStart,buf, vbLf) + 1
        
        jnl = Mid(buf, jnlStart, jnlEnd - jnlStart)
        jnl = Replace(jnl, "<span property=""v:category"">", "")
        jnl = Replace(jnl, "</span>", "")
        jnl = Replace(jnl, "</p>", "")
        jnl = Replace(jnl, vbLf, "")
        jnl = Replace(jnl, " ", "")
        
        
        '''' �d�b�擾 ''''''''''
        If cls = "�X" Then
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
        
        
        '''' ���X�R�A�擾 ''''''''''
        TscrStart = InStr(buf, "<strong class=""score"" rel=""v:rating""><span property=""v:average"">") + 64
        TscrEnd = InStr(TscrStart,buf, vbLf) + 1
        Tscr = Mid(buf, TscrStart, TscrEnd - TscrStart)
        Tscr = Replace(Tscr, "</span>", "")
        Tscr = Replace(Tscr, "</strong>", "")
        Tscr = Replace(Tscr, vbLf, "")
        Tscr = Replace(Tscr, " ", "")
        
        '''' ��X�R�A�擾 ''''''''''
        DscrStart = InStr(buf, "<span class=""dinner"">��̓_���F</span><em>") + 37
        DscrEnd = InStr(DscrStart,buf, vbLf) + 1
        Dscr = Mid(buf, DscrStart, DscrEnd - DscrStart)
        Dscr = Replace(Dscr, "</em>", "")
        Dscr = Replace(Dscr, vbLf, "")
        Dscr = Replace(Dscr, " ", "")
        
        '''' ���X�R�A�擾 ''''''''''
        LscrStart = InStr(buf, "<span class=""lunch"">���̓_���F</span><em>") + 36
        LscrEnd = InStr(LscrStart,buf, vbLf) + 1
        Lscr = Mid(buf, LscrStart, LscrEnd - LscrStart)
        Lscr = Replace(Lscr, "</em>", "")
        Lscr = Replace(Lscr, vbLf, "")
        Lscr = Replace(Lscr, " ", "")
        
        '�������c�t������
        
        '''' �A�N�Z�X�����擾 ''''''
        PVtotal = fsGetWordsBetween(buf, "�A�N�Z�X�� <em>", "</em>")
        
        '''' ��T�̃A�N�Z�X���擾 ''''''
        PVlastweek = fsGetWordsBetween(buf, "��T�̃A�N�Z�X���F</span><em>", "</em>")
        
        '''' ��X�T�̃A�N�Z�X���擾 ''''''
        PVlastweekbefore = fsGetWordsBetween(buf, "��X�T�̃A�N�Z�X���F</span><em>", "</em>")
        
        '�������c�t������
        
        '''' ���ϗ\�Z ''''
        
        YsnN = ""
        YsnD = ""
        
        YsnBuf = fsGetWordsBetween(buf, "<th>�\�Z", "</td>")
        
        YsnN = fsGetWordsBetween(YsnBuf, "[��]</span><span class=""price"">", "</span>")
        YsnN = Replace(YsnN, "�i", "")
        YsnN = Replace(YsnN, "�j", "")
        YsnN = Replace(YsnN, vbLf, "")
        YsnN = Replace(YsnN, vbCr, "")
        YsnN = Replace(YsnN, " ", "")
        YsnN = Replace(YsnN, "	", "")
        
        If YsnN = "" Then 
            
            YsnN = fsGetWordsBetween(YsnBuf, "<dt class=""budget-dinner"">��̗\�Z</dt>", "</dd>")
            YsnN = fsGetWordsBetween(YsnN, "class=""num""", "</dd>")
            YsnN = Replace(YsnN, "</a>", "")
            YsnN = Replace(YsnN, "property=""v:pricerange"">", "")
            YsnN = Replace(YsnN, "</em>", "")
            YsnN = Replace(YsnN, vbLf, "")
            YsnN = Replace(YsnN, vbCr, "")
            YsnN = Replace(YsnN, " ", "")
            YsnN = Replace(YsnN, "	", "")
            
        End If 
        
        
        YsnD = fsGetWordsBetween(YsnBuf, "[��]</span><span class=""price"">", "</span>")
        YsnD = Replace(YsnD, "�i", "")
        YsnD = Replace(YsnD, "�j", "")
        YsnD = Replace(YsnD, vbLf, "")
        YsnD = Replace(YsnD, vbCr, "")
        YsnD = Replace(YsnD, " ", "")
        YsnD = Replace(YsnD, "	", "")
        
        If YsnD = "" Then 
            
            YsnD = fsGetWordsBetween(YsnBuf, "<dt class=""budget-lunch"">���̗\�Z</dt>", "</dd>")
            YsnD = fsGetWordsBetween(YsnD, "class=""num""", "</dd>")
            YsnD = Replace(YsnD, "</a>", "")
            YsnD = Replace(YsnD, ">", "")
            YsnD = Replace(YsnD, "</em>", "")
            YsnD = Replace(YsnD, vbLf, "")
            YsnD = Replace(YsnD, vbCr, "")
            YsnD = Replace(YsnD, " ", "")
            YsnD = Replace(YsnD, "	", "")
            
        End If 
        
        '''' �c�Ǝ��ԕϐ� ''''
        OpnStart = InStr(buf, "<th>�c�Ǝ���</th>") + 13
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
        
        
        '''' ��x�� ''''
        HolStart = InStr(buf, "<th>��x��</th>") + 12
        HolEnd = InStr(HolStart,buf, vbLf) + 1
        HolEnd = InStr(HolEnd,buf, vbLf)
        Hol = Mid(buf, HolStart, HolEnd - HolStart)
        
        Hol = Replace(Hol, "<td>", "")
        Hol = Replace(Hol, "</td>", "")
        Hol = Replace(Hol, "<p>", "")
        Hol = Replace(Hol, "</p>", "")
        Hol = Replace(Hol, vbLf, "")
        Hol = Replace(Hol, " ", "")
        
        
        '''' �Ȑ� ''''
        CheStart = InStr(buf, "<th>�Ȑ�</th>") + 11
        
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
            
            ' �Ȑ��L�ڂȂ�
            Che = ""
            
        End If
        
        
        '''' �N���J ''''
        crcStart = InStr(buf, "<th>�J�[�h</th>") + 12
        
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
            
            ' �N���J�L�ڂȂ�
            crc = ""
            
        End If
        
        '''' �Ŋ�w ''''
        staStart = InStr(buf, "<th>��ʎ�i</th>") + 13
        
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
            
            ' �Ŋ�w�L�ڂȂ�
            sta = ""
            
        End If
        
        '''' �N�[�|�� ''''
        Cou = ""
        CouBufStart = InStr(buf, "<div class=""rstinfo-coupon"">") + 28
        
        If CouBufStart > 28 Then
            
            CouBufEnd = InStr(buf, "<div id=""rstinfo-actions"">")
            CouBuf = Mid(buf, CouBufStart, CouBufEnd - CouBufStart)
            
            ' ���ʂȃX�N���v�g�̍폜
            Do Until InStr(CouBuf, "//<![CDATA[") = 0
                
                CouBufStart = InStr(CouBuf, "//<![CDATA[")
                CouBufEnd = InStr(CouBuf, "//]]>") + 5
                
                CouBuf = Replace(CouBuf,Mid(CouBuf, CouBufStart, CouBufEnd - CouBufStart),"")
                
            Loop
            
            ' ���XML���폜
            Do Until InStr(CouBuf, "���̃N�[�|�������</a>") = 0
                
                CouBufStart = InStr(CouBuf, "���̃N�[�|�������</a>")
                
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
            
            ' �ŏI���H
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
            
            Cou = "�N�[�|�����Ȃ�"
            
        End If
        
        
        '''' �\��ەϐ� ''''
        ResStart = InStr(buf, "�\���")
        
        If ResStart = 0 Then
            
            ResStart = InStr(buf, "�\��s��")
            
            If ResStart = 0 Then
                
                Res = ""
                
            Else
                
                Res = "�\��s��"
                
            End If
            
        Else
            
            Res = "�\���"
            
        End If
        
        '''' �Z���ϐ� ''''
        AddStart = InStr(buf, "<th>�Z��</th>") + 11
        
        If AddStart > 11 Then
            
            AddEnd = InStr(buf, "<div class=""map-morelinks clearfix"">")
            
            If AddEnd <> 0 Then
                
                ' �Z�����{�W�I�R�[�h
                Add = Mid(buf, AddStart, AddEnd - AddStart)
                
                AddStart1 = InStr(Add, "<span property=""v:region"">") + 26
                AddEnd1 = InStr(Add, "<div class=""rst-map-wrap"">")
                Add1 = Mid(Add, AddStart1, AddEnd1 - AddStart1)
                
                Add1 = Replace(Add1, "</a>", "")
                Add1 = Replace(Add1, "</span>", "")
                Add1 = Replace(Add1, "</p>", "")
                Add1 = Replace(Add1, "<span property=""v:locality"">", "")
                Add1 = Replace(Add1, "<span property=""v:street-address"">", "")
                
                ' �ŏ��̃^�O������
                AddEnd1 = InStr(Add1, ">")
                Add1 = Replace(Add1,Left(Add1,AddEnd1),"")
                
                ' �]�v�ȃ^�O�͏���
                Do Until InStr(Add1, "<") = 0
                    AddStart1 = InStr(Add1, "<")
                    AddEnd1 = InStr(Add1, ">") + 1
                    Add1 = Replace(Add1,Mid(Add1,AddStart1,AddEnd1 - AddStart1), " ")
                    
                Loop
                
                Add1 = Replace(Add1, vbLf, "")
                Add1 = Replace(Add1, " ", "")
                Add1 = Replace(Add1, "�@", "")
                
                ' �W�I�R�[�h
                GeoStart = InStr(Add, "center=") + 7
                GeoEnd = InStr(Add, "&amp;markers=")
                
                Geo = Mid(Add, GeoStart, GeoEnd - GeoStart)
                
            Else
                
                ' �n�}�ڍׂȂ�
                Add1 = ""
                Geo = ""
                
            End If
            
        Else
            
            ' �n�}���Ȃ�
            Add1 = ""
            Geo = ""
            
        End If
        
        '''' �X�ܖ��J�i������ꍇ�͎擾 ''''
        If InStr(Title, "�i") > 0 Then
            
            KanaStart = InStr(Title, "�i") + 1
            KanaEnd = InStr(Title, "�j") 
            
            If KanaStart <> 0 And KanaEnd <> 0 And KanaStart < KanaEnd Then
                
                Kana = Mid(Title, KanaStart, KanaEnd - KanaStart)
                
                Title = Mid(Title, 1, KanaStart - 2)
                
            Else
                
                ' �ςȃf�[�^�͒��߂�
                Kana = ""
                
            End If
            
        Else
            
            ' �J�i�Ȃ��̂͒��߂�
            Kana = ""
            
        End If
        
        '''' ������𕪐� ''''
        memStart = InStr(buf, "���̃��X�g�����͐H�׃��O�X�܉���ɓo�^���Ă��邽�߁A���[�U�̊F�l�͕ҏW���邱�Ƃ��ł��܂���B") 
        
        If memStart > 0 Then
            
            ' ���
            memStart = InStr(buf, "<div class=""listing"">") 
            
            If memStart > 0 Then
                
                mem = "�������"
                
            Else
                
                mem = "�L�����"
                
            End If
            
        Else
            
            ' ����
            mem = "����"
            
        End If
        
        
        ''''''''''''���R�~��''''''''''''''''''''''
        
        comment = fsGetWordsBetween(buf, "<em class=""num"" property=""v:count"">", "</em>")
        comment = Replace(comment, "�i", "")
        comment = Replace(comment, "�j", "")
        comment = Replace(comment, vbLf, "")
        comment = Replace(comment, vbCr, "")
        comment = Replace(comment, " ", "")
        comment = Replace(comment, "	", "")
        
        
        ''''''''''''''''�l�b�g�\���''''''''''''''''
        
        
        If InStr(buf ,"_side_calendar_widget.js") = 0 Then 
            
            
            netBooking = "�l�b�g�\��s��"
            
        Else 
            
            netBooking = "�l�b�g�\���"
            
        End If 
        
        
        ''''''''''''''''preCoupon''''''''''''''''''''''
        Dim preCoupon
        
        
        If InStr(buf ,"<span class=""pcoupon-item-lead"">") <> 0 Then 
            
            preCoupon = "����"
        Else 
            preCoupon = "�Ȃ�"
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
        
        '''''''''''''''''''������񂠂�''''''''''''''''
        Dim offical
        
        If InStr(buf ,"<a class=""official-badge"">������񂠂�</a>") <> 0 Then 
            
            offical = "������񂠂�"
            
        Else 
            
            offical = "�������Ȃ�"
            
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
            
            Call WriteTextFile(MyFol & "\�L�^.txt", i, 1 )
            
        End If
        
    End If
    
Next

Set Http = Nothing

objFile.Close                               '�t�@�C�������

MsgBox "�������������܂����B"

'-------------------------------------------------------------------------------
' �ց@��      Private Function fsGetWordsBetween(ByVal P_sTargetWords As String, ByVal P_sStart As String, ByVal P_sEnd As String) As String
'
' ���@��      P_sTargetWords�F�Ώە�����        P_sStart�F�J�n����      P_sEnd�F�I������
'
' �߁@�l�@�@�@fsGetWordsBetween�F�����ň͂��Ă��镶������擾����B�i�J�n������������Ȃ������Ƃ���null��Ԃ��ďI���j
'
' ���@��      �z�[���y�[�W��URL�擾�v���O����
'
' ���@��      2013/08/09        Y.Hatsuda        �X�V
'--------------------------------------------------------------------------------

Private Function fsGetWordsBetween(ByVal P_sTargetWords, ByVal P_sStart, ByVal P_sEnd)
    
    ''''''''''''''�ϐ�''''''''''''''
    
    Dim lngPreWord		'��؂�O�̕����̕�����
    Dim lngEndWord		'��؂��̕����̕�����
    
    Dim lngStart
    Dim lngEnd
    
    ''''''''''''''''''''''''''''''''
    '�͂��Ă��镶���̕��������擾����
    lngPreWord = Len(P_sStart)
    lngEndWord = Len(P_sEnd)
    
    '�J�n������
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
' �ց@��      Private Sub WriteTextFile(ByVal P_sFilePath, ByVal P_sWriteWords, ByVal sNeedTime )
'
' ���@��      P_sFilePath�F�e�L�X�g�t�@�C���̃p�X        P_sWriteWords:���o������	sNeedTime:���Ԃ̏��o�����K�v�ȏꍇ��1�A����ȊO�̏ꍇ�͏����o�����s��Ȃ�
'
' �߁@�l�@�@�@�Ȃ�
'
' ���@��      �e�L�X�g�t�@�C���ւ̏������݁B�t�@�C�������݂��Ȃ��ꍇ�͍쐬���ď�������
'
' ���@��      2013/08/08        T.Kosaka        �V�K�쐬
'--------------------------------------------------------------------------------

Private Sub WriteTextFile(ByVal P_sFilePath, ByVal P_sWriteWords, ByVal sNeedTime )
    
    ''''''''''''''�ϐ�''''''''''''''
    
    Dim FSO		'�t�@�C���V�X�e���I�u�W�F�N�g
    Dim oLog	'�e�L�X�g
    Dim Ts		'�e�L�X�g�t�@�C��
    
    ''''''''''''''''''''''''''''''''
    '�C���X�^���X�̍쐬
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
