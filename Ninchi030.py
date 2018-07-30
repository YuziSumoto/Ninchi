#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import common

import datetime # 日付モジュール

from MstUser   import *   # 使用者マスタ
from DatNinchi030 import *   # 活動実績データ

class MainHandler(webapp2.RequestHandler):

  @login_required
#-------------------------------------------------------------
# 初期表示
#-------------------------------------------------------------
  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    if self.request.get('Year') != "": # パラメタ無し？
      Year = int(self.request.get('Year'))   # パラメタ取得
    else:
      Year = 2018

    Month = 4

    Recs = []

    WDatNinchi030 =  DatNinchi030()
    while True:
      Rec = WDatNinchi030.GetMonthList(Year,Month)
      Recs.append(Rec)
      if Month == 12:
        Year  += 1
        Month =  1
      else:
        Month += 1
      if Month == 4:
        break

    # 合計欄作成
    GRec = DatNinchi030() # 合計レコード
    GRec.Month      = 99
    GRec.LastSNinzu = 0
    GRec.LastSKaisu = 0
    GRec.LastHNinzu = 0
    GRec.LastHKaisu = 0

    for Rec in Recs:
      GRec.LastSNinzu += Rec.LastSNinzu
      GRec.SNinzu     += Rec.SNinzu
      GRec.Mokuhyo    += Rec.Mokuhyo
      GRec.LastSKaisu += Rec.LastSKaisu
      GRec.SKaisu     += Rec.SKaisu
      GRec.LastHNinzu += Rec.LastHNinzu
      GRec.HNinzu     += Rec.HNinzu
      GRec.LastHKaisu += Rec.LastHKaisu
      GRec.HKaisu     += Rec.HKaisu
      GRec.KaigiKaisu += Rec.KaigiKaisu
      GRec.KaigiNinzu += Rec.KaigiNinzu
    if GRec.Mokuhyo != 0:
      GRec.Tassei = int(float(GRec.SNinzu) / GRec.Mokuhyo * 100)
    else:
      GRec.Tassei = 0

    Recs.append(GRec)

    LblMsg = ""

    template_values = {
      'Year'   :Year - 1,
      'Recs'   :Recs,
      'LblMsg' :LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Ninchi030.html')
    self.response.out.write(template.render(path, template_values))
#-------------------------------------------------------------
# ボタン押下時
#-------------------------------------------------------------
  def post(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    Rec = {} # 画面受け渡し用領域
    LblMsg = ""

#    if self.request.get('BtnKettei')  != '':
#      ErrFlg,LblMsg = self.ChkInput() # 入力チェック
#      if ErrFlg == False: # エラー無し
#        LblMsg = u"更新完了しました。"
#        self.DBSet()
#        self.redirect("/Ninchi010/") # 一覧に戻る
#        return

#    ParaNames = self.request.arguments()  # 再表示用
#    for ParaName in ParaNames: # 前画面項目引き渡し
#      Rec[ParaName]    = self.request.get(ParaName)
#    self.ReDisp(Rec) # 再表示用

    template_values = {
      'Rec'     : Rec,
      'LblMsg'  : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Ninchi030.html')
    self.response.out.write(template.render(path, template_values))

#############################################################################
#------------------------------------------------------------------------------
  def ChkInput(self):   # 入力チェック

    ErrFlg = True
    LblMsg = ""

    if common.CheckTime(self,self.request.get('TxtZikoku_S')) == False:
      LblMsg = "開始時刻が正しくありません。(HH:MM)"
    elif common.CheckTime(self,self.request.get('TxtZikoku_E')) == False:
      LblMsg = "終了時刻が正しくありません。(HH:MM)"
    elif common.CheckDate(self,self.request.get('TxtBirthDay')) == False:
      LblMsg = "生年月日が正しくありません。(yyyy/mm/dd)"
    elif common.CheckDate(self,self.request.get('TxtZyusinKibou1')) == False:
      LblMsg = "受診希望日１件目が正しくありません。(yyyy/mm/dd)"
    elif common.CheckDate(self,self.request.get('TxtZyusinKibou2')) == False:
      LblMsg = "受診希望日２件目が正しくありません。(yyyy/mm/dd)"
    elif common.CheckDate(self,self.request.get('TxtZyusinKibou3')) == False:
      LblMsg = "受診希望日３件目が正しくありません。(yyyy/mm/dd)"
    else:
      ErrFlg = False

    return (ErrFlg,LblMsg)
#------------------------------------------------------------------------------
  def ReDisp(self,Rec):  # 画面再表示

    Rec["OptHouhou"   + self.request.get('OptHouhou')]   = "Checked"
    Rec["OptZyukyo"   + self.request.get('OptHouhou')]   = "Checked"
    Rec["OptSex"      + self.request.get('OptSex')]      = "Checked"
    Rec["OptZokugara" + self.request.get('OptZokugara')] = "Checked"

    for Ctr in range(1,5):
      if self.request.get('ChkTaiou' + str(Ctr)) == "on":
        Rec["ChkTaiou" + str(Ctr)] = "checked='checked'"

    return  # Recは構造体なんで参照→直接変更→戻り値不要

#------------------------------------------------------------------------------
  def DBGet(self,Key,Rec):  # データ読込

    DataRec = DatSoudan().GetRec(Key)

    if DataRec.Hizuke != None:
      Rec["TxtHizuke"]  = DataRec.Hizuke.strftime('%Y/%m/%d')

    if DataRec.Zikoku_S != None: # 開始時刻
      Rec["TxtZikoku_S"]  = DataRec.Zikoku_S.strftime('%H:%M')

    if DataRec.Zikoku_E != None: # 開始時刻
      Rec["TxtZikoku_E"]  = DataRec.Zikoku_E.strftime('%H:%M')
    
    Rec["TxtName"]   = DataRec.Name
    Rec["TxtTanto"]  = DataRec.Tanto
    if DataRec.Zyokyo != None:
      Rec["TxtZyokyo"]  = DataRec.Zyokyo
    Rec["TxtNaiyo"]  = DataRec.Naiyo
    if  DataRec.Houhou != None:
      Rec["OptHouhou" + str(DataRec.Houhou)] = "Checked"
    Rec["TxtHouhou"]  = DataRec.HouhouBikou
    if  DataRec.Zyukyo != None:
      Rec["OptZyukyo" + str(DataRec.Zyukyo)] = "Checked"
    Rec["TxtZyukyo"]  = DataRec.ZyukyoBikou
    if  DataRec.Sex != None:
      Rec["OptSex" + str(DataRec.Sex)] = "Checked"
    Rec["TxtZyusyo"]  = DataRec.Zyusyo

    if DataRec.BirthDay != None:
      Rec["TxtBirthDay"]  = common.GetWareki(DataRec.BirthDay) 
    
    Rec["TxtSoudanName"]  = DataRec.SoudanName # 相談者
    if  DataRec.Zokugara != None:
      Rec["OptZokugara" + str(DataRec.Zokugara)] = "Checked"
    Rec["TxtZokugara"]  = DataRec.ZokugaraBikou

    for Ctr in range(1,5):
      if getattr(DataRec,"TaiouKubun" + str(Ctr)) == True:
        Rec["ChkTaiou" + str(Ctr)] = "checked='checked'"
    Rec["TxtTaiou"]  = DataRec.Taiou

    for Ctr in range(1,4):   # 受診希望
      Hizuke = getattr(DataRec,"ZyusinKibou" + str(Ctr))
      if Hizuke != None:
        Rec["TxtZyusinKibou" + str(Ctr)] = Hizuke.strftime('%Y/%m/%d') 
      Rec["TxtZyusinBikou" + str(Ctr)] = getattr(DataRec,"ZyusinBikou" + str(Ctr))

    Rec["TxtRenYubin"]  = DataRec.RenYubin      # 連絡先
    Rec["TxtRenZyusyo"]  = DataRec.RenZyusyo
    Rec["TxtRenTel"]  = DataRec.RenTel

    Rec["TxtBikou"]  = DataRec.Bikou

    return  # Recは構造体なんで参照→直接変更→戻り値不要

#------------------------------------------------------------------------------
  def DBSet(self):  # データ保存

    Rec = DatSoudan()
    Hizuke = self.request.cookies.get('Hizuke', '') # Cookieより
    Rec.Hizuke  = datetime.datetime.strptime(Hizuke, '%Y/%m/%d') # 日付変換

    Key =  self.request.cookies.get('Key', '') # Cookieより

    if Key !="":
      Rec.DelRec(Key)
      Rec.Seq = 0

    if self.request.get('TxtZikoku_S') != "": # 開始時刻
      Hizuke = self.request.get('TxtZikoku_S')
      Rec.Zikoku_S  = datetime.datetime.strptime(Hizuke, '%H:%M') # 時刻変換

    if self.request.get('TxtZikoku_E') != "": # 終了時刻
      Hizuke = self.request.get('TxtZikoku_E')
      Rec.Zikoku_E  = datetime.datetime.strptime(Hizuke, '%H:%M') # 時刻変換

    Rec.Tanto        = self.request.get('TxtTanto')
    Rec.Zyokyo       = self.request.get('TxtZyokyo')
    Rec.Naiyo        = self.request.get('TxtNaiyo')
    Rec.Houhou       = int(self.request.get('OptHouhou'))
    Rec.HouhouBikou  = self.request.get('TxtHouhou')
    Rec.Zyukyo       = int(self.request.get('OptZyukyo'))
    Rec.ZyukyoBikou  = self.request.get('TxtZyukyo')
    Rec.Name         = self.request.get('TxtName')
    Rec.Sex          = int(self.request.get('OptSex'))
    Rec.Zyusyo       = self.request.get('TxtZyusyo')

    if self.request.get('TxtBirthDay') != "":  # 未入力時は無視ね
      setattr(Rec,"BirthDay",common.WarekiHenkan(self,self.request.get("TxtBirthDay")))
#      Hizuke = datetime.datetime.strptime(self.request.get('TxtBirthDay'), '%Y/%m/%d')
#      setattr(Rec,"BirthDay",Hizuke)

    Rec.SoudanName       = self.request.get('TxtSoudanName')
    Rec.Zokugara         = int(self.request.get('OptZokugara'))
    Rec.ZokugaraBikou    = self.request.get('TxtZokugara')

    for Ctr in range(1,5):
      if self.request.get('ChkTaiou' + str(Ctr)) == "on":
        setattr(Rec,"TaiouKubun" + str(Ctr),True)
      else:
        setattr(Rec,"TaiouKubun" + str(Ctr),False)
    Rec.Taiou        = self.request.get('TxtTaiou')

    for Ctr in range(1,4):
      if self.request.get('TxtZyusinKibou' + str(Ctr)) != "":  # 未入力時は無視ね
        Hizuke = datetime.datetime.strptime(self.request.get('TxtZyusinKibou' + str(Ctr)), '%Y/%m/%d')
        setattr(Rec,"ZyusinKibou" + str(Ctr),Hizuke)
      setattr(Rec,"ZyusinBikou" + str(Ctr),self.request.get('TxtZyusinBikou' + str(Ctr)))

    Rec.RenYubin    = self.request.get('TxtRenYubin')
    Rec.RenZyusyo    = self.request.get('TxtRenZyusyo')
    Rec.RenTel    = self.request.get('TxtRenTel')

    Rec.Bikou    = self.request.get('TxtBikou')

    Rec.put()
    
    return

#############################################################################
app = webapp2.WSGIApplication([
    ('/Ninchi030/', MainHandler)
], debug=True)
