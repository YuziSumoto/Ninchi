# -*- coding: UTF-8 -*-
from google.appengine.ext import db

class MstUser(db.Model):
  Name              = db.StringProperty(multiline=False)      # ユーザ名

  def ChkUser(self,Name):


    Sql  =   "SELECT * FROM MstUser"
    Sql  +=  " Where Name = '" + Name + "'"
    Query = db.GqlQuery(Sql)
    if Query.count() == 0:
      RetFlg = False
    else:
      RetFlg = True

    return RetFlg

