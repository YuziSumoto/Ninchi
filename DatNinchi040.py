# -*- coding: UTF-8 -*-
from google.appengine.ext import db

import datetime # 日付モジュール

class DatNinchi040(db.Model):
  Hizuke            = db.DateTimeProperty(auto_now_add=False) # 年月日
  Zissi             = db.BooleanProperty(default=False)               # 実施フラグ
  Basyo             = db.StringProperty(multiline=False,default="")   # 場所
  Ninzu             = db.IntegerProperty(default=0)                   # 参加人数
  
  def GetAll(self): # 全データ取得

    Sql =  "SELECT * FROM DatNinchi040"
    Sql += " Order By Hizuke,Basyo"
    Snap = db.GqlQuery(Sql)
    Recs  = Snap.fetch(Snap.count())

    return Recs

  def GetRec(self,Key): # 指定キーのデータ取得

    if Key == "":
      return DatNinchi040()
    Sql =  "SELECT * FROM DatNinchi040"
    Sql +=  " Where __key__ = KEY('" + str(Key) + "')"
    Snap = db.GqlQuery(Sql)
    Rec = Snap.fetch(Snap.count())

    return Rec[0]

  def DelRec(self,Key): # 指定患者,指定日,指定Seq削除

    Sql =  "SELECT * FROM DatNinchi040"
    Sql +=  " Where __key__ = KEY('" + str(Key) + "')"
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

    return
