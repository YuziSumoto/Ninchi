#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import webapp2

import os
from google.appengine.ext.webapp import template

from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import common

import datetime # 日付モジュール

from MstUser   import *      # 使用者マスタ
from DatNinchi040 import *   # 活動報告データ

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

    if self.request.get('Key') != "": # パラメタ無し？
      Key = self.request.get('Key')   # パラメタ取得
    else:
      Key = ""
    cookieStr = 'Key=' + str(Key) + ';'     # Cookie保存
    self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    LblMsg = ""

    template_values = {
      'Rec'    :DatNinchi040().GetRec(Key),
      'LblMsg' :LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Ninchi041.html')
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
       self.DBSet()
       self.redirect("/Ninchi040/") # 一覧に戻る
       return

    if self.request.get('BtnDel')  != '':
      Key = self.request.cookies.get('Key', '') # Cookieより
      if Key != "":
        DatNinchi040().DelRec(Key)
      self.redirect("/Ninchi040/") # 一覧に戻る
      return

    template_values = {
      'Rec'     : Rec,
      'LblMsg'  : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Ninchi041.html')
    self.response.out.write(template.render(path, template_values))

#------------------------------------------------------------------------------
  def DBSet(self):  # データ保存
 
    Key = self.request.cookies.get('Key', '') # Cookieより

    if Key != "":
      DatNinchi040().DelRec(Key)

    Rec = DatNinchi040()

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
    ('/Ninchi041/', MainHandler)
], debug=True)
