# -*- coding: UTF-8 -*-
from google.appengine.ext import db

import datetime # 日付モジュール

class DatNinchi030(db.Model):
  Hizuke            = db.DateTimeProperty(auto_now_add=False) # 年月(1日)
  SNinzu            = db.IntegerProperty(default=0)   # 新規相談人数
  Mokuhyo           = db.IntegerProperty(default=0)   # 目標値
  SKaisu            = db.IntegerProperty(default=0)   # 総相談回数
  HNinzu            = db.IntegerProperty(default=0)   # 新規訪問人数
  HKaisu            = db.IntegerProperty(default=0)   # 訪問回数
  KaigiKaisu        = db.IntegerProperty(default=0)   # 会議回数
  KaigiNinzu        = db.IntegerProperty(default=0)   # 検討人数
  
  def GetMonthList(self,Year,Month): # 指定月のデータ取得

    Sql =  "SELECT * FROM DatNinchi030"
    Sql += " Where Hizuke = DATE('" + str(Year) + "-" + str(Month) + "-01')"
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      Rec  = DatNinchi030()
    else:
      Rec  = Snap.fetch(1)[0]

    Sql =  "SELECT * FROM DatNinchi030"
    Sql += " Where Hizuke = DATE('" + str(int(Year)-1) + "-" + str(Month) + "-01')"
    Snap = db.GqlQuery(Sql)
    if Snap.count() == 0:
      LastRec  = DatNinchi030()
    else:
      LastRec  = Snap.fetch(1)[0]

    Rec.Year       = Year
    Rec.Month      = Month
    Rec.LastSNinzu = LastRec.SNinzu
    Rec.LastSKaisu = LastRec.SKaisu
    Rec.LastHNinzu = LastRec.HNinzu
    Rec.LastHKaisu = LastRec.HKaisu
    if Rec.Mokuhyo != 0:
      Rec.Tassei = int(float(Rec.SNinzu) / Rec.Mokuhyo * 100)
    else:
      Rec.Tassei = 0

    return Rec

  def DelRec(self,Year,Month): # 指定患者,指定日,指定Seq削除

    Sql =  "SELECT * FROM DatNinchi030"
    Sql += " Where Hizuke = DATE('" + str(Year) + "-" + str(Month) + "-01')"
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

    return

