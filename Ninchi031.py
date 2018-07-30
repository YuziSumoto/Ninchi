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
      Year = self.request.get('Year')   # パラメタ取得

    if self.request.get('Month') != "": # パラメタ無し？
      Month = self.request.get('Month')   # パラメタ取得

    cookieStr = 'Year=' + str(Year) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))
    cookieStr = 'Month=' + str(Month) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    LblMsg = ""

    template_values = {
      'Rec'    :DatNinchi030().GetMonthList(Year,Month),
      'Year'   :Year,
      'Month'  :Month,
      'LblMsg' :LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Ninchi031.html')
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

    if self.request.get('BtnKettei')  != '':
#      ErrFlg,LblMsg = self.ChkInput() # 入力チェック
#      if ErrFlg == False: # エラー無し
#        LblMsg = u"更新完了しました。"
       self.DBSet()
       Year = int(self.request.cookies.get('Year', ''))
       if int(self.request.cookies.get('Month', '')) < 4:
         Year -= 1
       self.redirect("/Ninchi030/?Year=" + str(Year) ) # 一覧に戻る
       return

#    ParaNames = self.request.arguments()  # 再表示用
#    for ParaName in ParaNames: # 前画面項目引き渡し
#      Rec[ParaName]    = self.request.get(ParaName)
#    self.ReDisp(Rec) # 再表示用

    template_values = {
      'Rec'     : Rec,
      'LblMsg'  : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Ninchi031.html')
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
  def DBSet(self):  # データ保存
 
    Year = self.request.cookies.get('Year', '') # Cookieより
    Month = self.request.cookies.get('Month', '') # Cookieより

    DatNinchi030().DelRec(Year,Month)

    Rec = DatNinchi030()
    Rec.Hizuke =datetime.datetime.strptime(Year + "-" + Month + "-01", '%Y-%m-%d')

    Dic = Rec.properties()

    ParaNames = self.request.arguments()
    for ParaName in ParaNames: # 前画面項目引き渡し
      if ParaName not in Dic: # 該当文字列が辞書にない
        ParaName = ParaName # 何もしない
      elif  type(Dic[ParaName]) == db.DateTimeProperty and self.request.get(ParaName)!= "": # 日付型
        setattr(Rec,ParaName,datetime.datetime.strptime(self.request.get(ParaName).replace("/","-"), '%Y-%m-%d'))
      elif  type(Dic[ParaName]) == db.IntegerProperty and self.request.get(ParaName)!= "": # 数値型
        setattr(Rec,ParaName,int(self.request.get(ParaName)))
      elif  type(Dic[ParaName]) == db.BooleanProperty:
        if self.request.get(ParaName) == "True":
          setattr(Rec,ParaName,True)
        else:
          setattr(Rec,ParaName,False)
      else:
        setattr(Rec,ParaName,self.request.get(ParaName))

    Rec.put()
    
    return

#############################################################################
app = webapp2.WSGIApplication([
    ('/Ninchi031/', MainHandler)
], debug=True)
