# -*- coding: UTF-8 -*-
from google.appengine.ext import db

class DatSoudan(db.Model):
  Hizuke            = db.DateTimeProperty(auto_now_add=False) # 相談日
  Seq               = db.IntegerProperty()                    # 相談番号
  Zikoku_S          = db.DateTimeProperty(auto_now_add=False) # 開始日時
  Zikoku_E          = db.DateTimeProperty(auto_now_add=False) # 終了日時
  Tanto             = db.StringProperty(multiline=False)      # 担当者
  Houhou            = db.IntegerProperty()                    # 相談方法
  HouhouBikou       = db.StringProperty(multiline=False)      # 相談方法備考
  Zyukyo            = db.IntegerProperty()                    # 住居状況
  ZyukyoBikou       = db.StringProperty(multiline=False)      # 住居状況備考
  Name              = db.StringProperty(multiline=False)      # 対象者名
  Sex               = db.IntegerProperty()                    # 性別
  Zyusyo            = db.StringProperty(multiline=False)      # 住所
  BirthDay          = db.DateTimeProperty(auto_now_add=False) # 生年月日
  SoudanName        = db.StringProperty(multiline=False)      # 相談者名
  Zokugara          = db.IntegerProperty()                    # 続柄
  ZokugaraBikou     = db.StringProperty(multiline=False)      # 続柄備考
  Naiyo             = db.StringProperty(multiline=True)       # 内容
  TaiouKubun1       = db.BooleanProperty()                    # 対応区分1
  TaiouKubun2       = db.BooleanProperty()                    # 対応区分1
  TaiouKubun3       = db.BooleanProperty()                    # 対応区分1
  TaiouKubun4       = db.BooleanProperty()                    # 対応区分1
  Taiou             = db.StringProperty(multiline=True)       # 対応内容
  ZyusinKibou1      = db.DateTimeProperty(auto_now_add=False) # 受診希望日1
  ZyusinBikou1      = db.StringProperty(multiline=False)      # 受診備考1
  ZyusinKibou2      = db.DateTimeProperty(auto_now_add=False) # 受診希望日2
  ZyusinBikou2      = db.StringProperty(multiline=False)      # 受診備考2
  ZyusinKibou3      = db.DateTimeProperty(auto_now_add=False) # 受診希望日3
  ZyusinBikou3      = db.StringProperty(multiline=False)      # 受診備考3
  RenYubin          = db.StringProperty(multiline=False)      # 連絡先
  RenZyusyo         = db.StringProperty(multiline=False)      # 住所
  RenTel            = db.StringProperty(multiline=False)      # 電話番号
  Bikou             = db.StringProperty(multiline=True)       # 備考

  def GetDayList(self,Hizuke): # 指定日のデータ取得

    Sql =  "SELECT * FROM DatSoudan"
    Sql += " Where Hizuke = DATE('" + Hizuke.replace("/","-") + "')"
    Sql += "    Order By Seq"
    Snap = db.GqlQuery(Sql)
    Rec  = Snap.fetch(Snap.count())

    return Rec

  def GetLastSeq(self,Hizuke): # 指定日付最終Seq取得

    Sql =  "SELECT Seq FROM DatSoudan"
    Sql += " Where Hizuke = DATE('" + Hizuke.replace("/","-") + "')"
    Sql += "    Order By Seq Desc" # 大きい順
    Snap = db.GqlQuery(Sql)
    if  Snap.count() == 0:  # 当日データなければ 0
      LastSeq = 0
    else:
      LastSeq = Snap.fetch(1)[0].Seq # 最大のSeq

    return LastSeq

  def GetRec(self,Hizuke,Seq): # 指定日,指定番号のデータ取得

    Sql =  "SELECT * FROM DatSoudan"
    Sql += " Where Hizuke = DATE('" + Hizuke.replace("/","-") + "')"
    Sql += "  And  Seq    = " + str(Seq)
    Snap = db.GqlQuery(Sql)
    Rec = Snap.fetch(Snap.count())


  def DelRec(self,Hizuke,Seq): # 指定患者,指定日,指定Seq削除

    Sql =  "SELECT * FROM DatSoudan"
    Sql += " Where Hizuke = DATE('" + Hizuke.replace("/","-") + "')"
    Sql += "  And  Seq    = " + Seq
    Snap = db.GqlQuery(Sql)
    for Rec in Snap:
       Rec.delete()

    return
