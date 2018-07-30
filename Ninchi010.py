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
from DatSoudan import *   # 相談記録

class MainHandler(webapp2.RequestHandler):

  @login_required

  def get(self):

    user = users.get_current_user() # ログオン確認
    if MstUser().ChkUser(user.email()) == False:
      self.redirect(users.create_logout_url(self.request.uri))
      return
    if self.request.get('Hizuke') == "": # パラメタ無し？
      Hizuke = self.request.cookies.get('Hizuke', '') # Cookieより
    else:
      Hizuke = self.request.get('Hizuke')   # パラメタ取得
      cookieStr = 'Hizuke=' + self.request.get('Hizuke') + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    LblMsg = "記録を選択するか、新規作成を押してください"

    template_values = {
      'Hizuke':Hizuke,
      'Recs'  :DatSoudan().GetAll(),
      'LblMsg': LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Ninchi010.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    LblMsg = " "

    for param in self.request.arguments(): 
      if "BtnSelect" in param:  # 更新ボタン？
        Parm = "?Key=" + param.replace("BtnSelect","")  # Cookieより
        self.redirect("/Ninchi020/" + Parm) #
      if "BtnDel" in param:  # 削除ボタン？
        DatSoudan().DelRec(param.replace("BtnDel",""))

    if self.request.get('BtnAdd')  != '':
      Parm = "?Hizuke=" + self.request.cookies.get('Hizuke', '') # Cookieより
      self.redirect("/Ninchi020/" + Parm) # 
      return

    Hizuke = self.request.cookies.get('Hizuke', '') # Cookieより

    template_values = {
      'Hizuke':Hizuke,
      'Recs'  :DatSoudan().GetAll(),
      'LblMsg': LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Ninchi010.html')
    self.response.out.write(template.render(path, template_values))

####################################################################################################


app = webapp2.WSGIApplication([
    ('/Ninchi010/', MainHandler)
], debug=True)
