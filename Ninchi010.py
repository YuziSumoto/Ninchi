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

    Rec = {} # 画面受け渡し用領域

    if self.request.get('Hizuke') == "": # パラメタ無し？
      Rec["TxtHizuke"] = self.request.cookies.get('Hizuke', '') # Cookieより
    else:
      Rec["TxtHizuke"] = self.request.get('Hizuke')   # パラメタ取得
      cookieStr = 'Hizuke=' + self.request.get('Hizuke') + ';'     # Cookie保存
      self.response.headers.add_header('Set-Cookie', cookieStr.encode('shift-jis'))

    LblMsg = "記録を選択するか、新規作成を押してください"

    strTable  =  self.TableSet(Rec["TxtHizuke"])

    template_values = {
      'Rec'     :Rec,
      'StrTable':strTable,
      'LblMsg': LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Ninchi010.html')
    self.response.out.write(template.render(path, template_values))

  def post(self):

    LblMsg = " "

    if self.request.get('BtnSelect')  != '':
      Parm =  "?Hizuke=" + self.request.cookies.get('Hizuke', '') # Cookieより
      Parm += "&Seq=" + self.request.get('BtnSelect', '') # Cookieより
      self.redirect("/Ninchi020/" + Parm) #
      return

    for param in self.request.arguments(): 
      if "BtnDel" in param:  # 削除ボタン？
        DatSoudan().DelRec(self.request.cookies.get('Hizuke', ''),param.replace("BtnDel",""))

    if self.request.get('BtnAdd')  != '':
      Parm = "?Hizuke=" + self.request.cookies.get('Hizuke', '') # Cookieより
      self.redirect("/Ninchi020/" + Parm) # 
      return

    strTable  =  self.TableSet(self.request.cookies.get('Hizuke', ''))

    template_values = {
      'StrTable':strTable,
      'LblMsg': LblMsg
      }
    path = os.path.join(os.path.dirname(__file__), 'Ninchi010.html')
    self.response.out.write(template.render(path, template_values))

####################################################################################################

#  テーブルセット
  def TableSet(self,Hizuke):

    retStr = ""

    Snap = DatSoudan().GetDayList(Hizuke)

#    for Ctr in range(1,10):
    for Rec in Snap:

      retStr += "<TR>"

      retStr += "<TD>"    # 更新ボタン（患者コード)
      retStr += "<input type='submit' value = '"
      retStr += "{0:02d}".format(Rec.Seq)
      retStr += "' name='BtnSelect"
      retStr += "' style='width:80px'>"
      retStr += "</TD>"

      retStr += "<TD>"    # 患者名
      retStr += Rec.Name
      retStr += "</TD>"

      retStr += "<TD>"    # 印刷ボタン（患者コード)
      retStr += u"<input type='button' value = '印刷'"
      retStr += "onclick='window.open("
      retStr += '"/Ninchi025/'
      retStr += "?Hizuke=" + Rec.Hizuke.strftime('%Y/%m/%d')
      retStr += "&Seq=" + str(Rec.Seq)
      retStr += '"'
      retStr += ");'"
      retStr += " style='width:50px'>"
      retStr += "</TD>"
      retStr += "<TD>"    # 削除ボタン（患者コード)
      retStr += u"<input type='submit' value = '削除'"
      retStr += "' name='BtnDel" 
      retStr += str(Rec.Seq)
      retStr += "' style='width:50px'>"
      retStr += "</TD>"

      retStr += "</TR>"

    return retStr

app = webapp2.WSGIApplication([
    ('/Ninchi010/', MainHandler)
], debug=True)