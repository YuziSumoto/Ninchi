#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

#import os
from google.appengine.ext.webapp import template
from google.appengine.api import users

import common

import datetime
import time
from calendar import monthrange
import locale

import xlwt
import StringIO

from MstUser   import *   # 使用者マスタ
from DatSoudan import *   # 相談記録データ

class MainHandler(webapp2.RequestHandler):

  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return
    
    Key = self.request.get('Key')   # パラメタ取得

    WorkBook =  self.TableDataSet(Key)

    self.response.headers['Content-Type'] = 'application/ms-excel'
    self.response.headers['Content-Transfer-Encoding'] = 'Binary'
    self.response.headers['Content-disposition'] = 'attachment; filename="Ninchi025.xls"'
    WorkBook.save(self.response.out)

  def TableDataSet(self,Key):

    Styles = self.SetStyles()

    WorkBook = xlwt.Workbook()  # 新規Excelブック

    WorkSheet = WorkBook.add_sheet(u'相談記録')  # ダミーシート
    self.SetPrintParam(WorkSheet) # 用紙サイズ・余白設定
    WorkSheet.write_merge(1,1,1,7,u'呉認知症疾患医療センター　認知症初期集中支援チーム',Styles["Style002"])
    WorkSheet.write_merge(2,2,1,7,u'相談記録',Styles["Style001"])

    for Ctr in range(4,40):  # 行幅セット
      WorkSheet.row(Ctr).height_mismatch = 1
      WorkSheet.row(Ctr).height = 500

    for Ctr in range(1,10):  # 列幅セット
      WorkSheet.col(Ctr).width = 10 * 400 

    # 見出し列セット

    WorkSheet.write( 3,1,u"日時",Styles["Style002"])
    WorkSheet.write( 4,1,u"相談方法",Styles["Style002"])

    WorkSheet.write_merge(5,6,1 ,1,u"対象者",Styles["Style002"])
    WorkSheet.write_merge(7,8,1 ,1,u"相談者",Styles["Style002"])

    WorkSheet.write_merge(9,16,1 ,1,u"相談経緯",Styles["Style002"])
    WorkSheet.write_merge(17,23,1 ,1,u"相談内容",Styles["Style002"])
    WorkSheet.write_merge(24,27,1 ,1,u"対応",Styles["Style002"])

    WorkSheet.write_merge(28,30,1,1,u"受診希望日",Styles["Style002"])

    WorkSheet.write_merge(31,32,1,1,u"連絡先",Styles["Style002"])
    WorkSheet.write_merge(33,36,1,1,u"備考",Styles["Style002"])

    # ここからデータ
    Rec = DatSoudan().GetRec(Key)    # データ読み込み

    WorkSheet.write(0,1,Rec.Hizuke.strftime('%Y/%m/%d'))
    WorkSheet.write(0,2,str(Rec.Seq))

    Hizuke = Rec.Hizuke
    OutStr = Hizuke.strftime('%Y') + u"年 "  # 日付変換
    OutStr += Hizuke.strftime('%m') + u"月 "  # 日付変換
    OutStr += Hizuke.strftime('%d') + u"日 "  # 日付変換
    if Rec.Zikoku_S != None:
      OutStr += Rec.Zikoku_S.strftime('%H:%M') # 時刻変換
    if Rec.Zikoku_E != None:
      OutStr += u"～" + Rec.Zikoku_E.strftime('%H:%M') # 時刻変換
    WorkSheet.write_merge(3,3,2 ,4,OutStr,Styles["Style002"])

    WorkSheet.write_merge(3,3,5 ,5,u"担当者",Styles["Style002"])
    WorkSheet.write_merge(3,3,6 ,7,Rec.Tanto,Styles["Style003"])

    if   Rec.Houhou == 1:   # 相談方法
      OutStr = u"電話"
    elif Rec.Houhou == 2:
      OutStr = u"受診"
    elif Rec.Houhou == 3:
      OutStr = u"その他"
    else:
      OutStr = ""
    if Rec.HouhouBikou != "":
      OutStr += "(" + Rec.HouhouBikou + ")"
    WorkSheet.write_merge(4,4,2 ,4,OutStr,Styles["Style003"])

    WorkSheet.write_merge(4,4,5 ,5,u"住居状況",Styles["Style002"])
    if   Rec.Zyukyo == 1:   # 住居状況
      OutStr = u"自宅"
    elif Rec.Houhou == 2:
      OutStr = u"入所・入院"
    elif Rec.Houhou == 3:
      OutStr = u"その他"
    else:
      OutStr = ""
    if Rec.ZyukyoBikou != "":
      OutStr += "(" + Rec.ZyukyoBikou + ")"
    WorkSheet.write_merge(4,4,6 ,7,OutStr,Styles["Style003"])

    # 対象者
    WorkSheet.write_merge(5,5,2 ,2,u"氏名",Styles["Style002"])
    WorkSheet.write_merge(5,5,3 ,4,Rec.Name,Styles["Style003"])

    WorkSheet.write_merge(5,5,5 ,5,u"性別",Styles["Style002"])
    if Rec.Sex == 1:
      OutStr = u"男"
    else:
      OutStr = u"女"
    WorkSheet.write_merge(5,5,6 ,7,OutStr,Styles["Style002"])

    WorkSheet.write_merge(6,6,2 ,2,u"住所",Styles["Style002"])
    WorkSheet.write_merge(6,6,3 ,4,Rec.Zyusyo,Styles["Style003"])

    WorkSheet.write_merge(6,6,5 ,5,u"生年月日",Styles["Style002"])
    if Rec.BirthDay != None:
      OutStr =  common.GetWareki(Rec.BirthDay)
    else:
      OutStr = " " # 何か書かないと枠線引かないよ
    WorkSheet.write_merge(6,6,6 ,7,OutStr,Styles["Style002"])

    # 相談者
    WorkSheet.write_merge(7,7,2 ,2,u"氏名",Styles["Style002"])
    WorkSheet.write_merge(7,7,3 ,7,Rec.SoudanName,Styles["Style003"])

    if   Rec.Zokugara == 1:   # 続柄
      OutStr = u"本人"
    elif Rec.Houhou == 2:
      OutStr = u"家族"
    elif Rec.Houhou == 3:
      OutStr = u"友人"
    elif Rec.Houhou == 4:
      OutStr = u"その他"
    else:
      OutStr = ""
    if Rec.ZokugaraBikou != "":
      OutStr += "(" + Rec.ZokugaraBikou + ")"
    WorkSheet.write_merge(8,8,2 ,7,OutStr,Styles["Style003"])

    # 相談状況
    OutStr = Rec.Zyokyo  # .replace('\r\n','\n') # 改行コード対応　これないとEXCELは改行しない
    WorkSheet.write_merge(9,16,2 ,7,OutStr,Styles["Style004"])

    # 相談内容
#    OutStr = Rec.Naiyo.replace(('\r'or'\n'),'\r\n') # 改行コード対応　これないとEXCELは改行しない
    OutStr = Rec.Naiyo  # .replace('\r\n','\n') # 改行コード対応　これないとEXCELは改行しない
#    WorkSheet.write_merge(9,23,2 ,7,OutStr,Styles["Style004"])
    WorkSheet.write_merge(17,23,2 ,7,OutStr,Styles["Style004"])

    # 対応
    OutStr = ""
    if   Rec.TaiouKubun1 == True:
      OutStr += u" 電話相談のみ"
    if   Rec.TaiouKubun2 == True:
      OutStr += u" 受診"
    if   Rec.TaiouKubun3 == True:
      OutStr += u" 入院"
    if   Rec.TaiouKubun4 == True:
      OutStr += u" その他"
    WorkSheet.write_merge(24,24,2 ,7,OutStr,Styles["Style003"])
    WorkSheet.write_merge(25,27,2 ,7,Rec.Taiou,Styles["Style004"])

    # 受診希望日
    for Ctr in range(1,4):  # ３までなら４を！
      OutRow = 27 + Ctr # 出力行
      if getattr(Rec,"ZyusinKibou" + str(Ctr)) != None: # 受診希望日
        OutStr = getattr(Rec,"ZyusinKibou" + str(Ctr)).strftime('%Y/%m/%d') # 日付変換
      else:
        OutStr = " "
      WorkSheet.write_merge(OutRow,OutRow,2 ,2,OutStr,Styles["Style002"])
      OutStr = getattr(Rec,"ZyusinBikou" + str(Ctr))  # 受診備考
      WorkSheet.write_merge(OutRow,OutRow,3 ,7,OutStr,Styles["Style003"])

    # 連絡先
    WorkSheet.write_merge(31,31,2 ,2,u"氏名",Styles["Style002"])
    WorkSheet.write_merge(31,31,3 ,7,Rec.RenYubin,Styles["Style003"])
    WorkSheet.write_merge(32,32,2 ,2,u"住所",Styles["Style002"])
    WorkSheet.write_merge(32,32,3 ,5,Rec.RenZyusyo,Styles["Style003"])
    WorkSheet.write_merge(32,32,6 ,6,u"電話番号",Styles["Style002"])
    WorkSheet.write_merge(32,32,7 ,7,Rec.RenTel,Styles["Style003"])

    # 備考
    WorkSheet.write_merge(33,36,2 ,7,Rec.Bikou,Styles["Style004"])

    return WorkBook # 終わり

#------------------------------------------------------------------------------
  def SetStyles(self):
  
    Styles = {}

    # タイトル
    Style = self.SetStyle(False,"THIN",False,False,False,xlwt.Alignment.HORZ_CENTER) 
    font = xlwt.Font() # Create the Font
    font.height = 450
    Style.font = font # Apply the Font to the Style
    Styles["Style001"] = Style

    # 全囲み センタ
    Style = self.SetStyle("THIN","THIN","THIN","THIN",xlwt.Alignment.VERT_CENTER,xlwt.Alignment.HORZ_CENTER)
    font = xlwt.Font() # Create the Font
    font.height = 200
    Style.font = font # Apply the Font to the Style
    Styles["Style002"] = Style

    # 囲み無し センタ
    Style = self.SetStyle(False,False,False,False,xlwt.Alignment.VERT_CENTER,xlwt.Alignment.HORZ_CENTER)
    font = xlwt.Font() # Create the Font
    font.height = 250
    Style.font = font # Apply the Font to the Style
    Styles["Style003"] = Style

    # 全囲み 左寄せ
    Style = self.SetStyle("THIN","THIN","THIN","THIN",xlwt.Alignment.VERT_CENTER,xlwt.Alignment.HORZ_LEFT)
    font = xlwt.Font() # Create the Font
    font.height = 200
    Style.font = font # Apply the Font to the Style
    Styles["Style003"] = Style

    # 全囲み 左上寄せ
    Style = self.SetStyle("THIN","THIN","THIN","THIN",xlwt.Alignment.VERT_TOP,xlwt.Alignment.HORZ_LEFT)
    font = xlwt.Font() # Create the Font/
    font.height = 200
    Style.font = font # Apply the Font to the Style
    Styles["Style004"] = Style

    return Styles

  def SetStyle(self,Top,Bottom,Right,Left,Vert,Horz):  # セルスタイルセット

    Style = xlwt.XFStyle()
    Border = xlwt.Borders()
    if Top == "THIN":
      Border.top     = xlwt.Borders.THIN
    elif Top == "DOTTED":
      Border.top     = xlwt.Borders.DOTTED

    if Bottom == "THIN":
      Border.bottom  = xlwt.Borders.THIN
    elif Bottom == "DOTTED":
      Border.bottom     = xlwt.Borders.DOTTED

    if   Left == "THIN":
      Border.left    = xlwt.Borders.THIN
    elif Left == "DOTTED":
      Border.left    = xlwt.Borders.DOTTED

    if   Right == "THIN":
      Border.right   = xlwt.Borders.THIN
    elif Right == "DOTTED":
      Border.right   = xlwt.Borders.DOTTED

    Style.borders = Border

    Alignment      = xlwt.Alignment()

    Alignment.wrap = 1 # これないとセル内改行が効かない
#    if Vert != False:
    Alignment.vert = Vert
#    if Horz != False:
    Alignment.horz = Horz

    Style.alignment = Alignment

    return Style

  def SetPrintParam(self,WorkSheet): # 用紙サイズ・余白設定
#    WorkSheet.set_paper_size_code(13) # B5
    WorkSheet.set_paper_size_code(9) # A4
    WorkSheet.set_portrait(1) # 縦
#    WorkSheet.set_portrait(2) # 横
    WorkSheet.top_margin = 0.0 / 2.54    # 1インチは2.54cm
    WorkSheet.bottom_margin = 0.5 / 2.54    # 1インチは2.54cm
    WorkSheet.left_margin = 1.0 / 2.54    # 1インチは2.54cm
    WorkSheet.right_margin = 0.5 / 2.54    # 1インチは2.54cm
    WorkSheet.header_str = ''
    WorkSheet.footer_str = ''
    WorkSheet.fit_num_pages = 1
#    WorkSheet.fit_height_to_pages = 0
#    WorkSheet.fit_width_to_pages = 1
#    WorkSheet.print_scaling = 100
    return

################################################################################

app = webapp2.WSGIApplication([
    ('/Ninchi025/', MainHandler)
], debug=True)
