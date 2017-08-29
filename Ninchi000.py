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

class MainHandler(webapp2.RequestHandler):

  @login_required

  def get(self):

#    DynaUser =  MstUser()
#    DynaUser.Name = "gotou@kangosien.com"
#    DynaUser.put()

    LblMsg = ""

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return

    if self.request.get('TxtHizuke') == "":
      TxtHizuke = datetime.datetime.now().strftime('%Y/%m/%d') # 今日の日付
    else:
      TxtHizuke = self.request.get('TxtHizuke')

    if self.request.get('BtnNinchi010')  != '':
      ErrFlg,LblMsg = self.ChkInput() # 入力チェック
      if ErrFlg == False: # エラー無し
        Parm = "?Hizuke=" + self.request.get('TxtHizuke')
        self.redirect("/Ninchi010/" + Parm ) # 一覧画面へ
        return
        

    if self.request.get('BtnLogout')  != '':
      self.redirect(users.create_logout_url(self.request.uri))
      return

    template_values = {
      'TxtHizuke' : TxtHizuke,
      'LblMsg'    : LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Ninchi000.html')
    self.response.out.write(template.render(path, template_values))

################################################################################
#--------------#
#-入力チェック #
#--------------#
  def ChkInput(self):   # 入力チェック

    ErrFlg = True
    LblMsg = ""

    if self.request.get('TxtHizuke') == "":
      LblMsg = "日付が未入力です。"
    elif common.CheckDate(self,self.request.get('TxtHizuke')) == False:
      LblMsg = "日付が正しくありません。"
    else:
      ErrFlg = False

    return (ErrFlg,LblMsg)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Ninchi000/', MainHandler)
], debug=True)
