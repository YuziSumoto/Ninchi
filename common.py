# -*- coding: UTF-8 -*-

import datetime # 日付モジュール

def CheckDate(self,Hizuke): # 日付チェック

  if Hizuke == "":
    return True

  try:
      newDate=datetime.datetime.strptime(Hizuke,"%Y/%m/%d")
      return True
  except ValueError:
      return False

def CheckTime(self,Zikoku): # 時刻チェック

  if Zikoku == "":
    return True

  try:
      newDate=datetime.datetime.strptime(Zikoku,"%H:%M")
      return True
  except ValueError:
      return False

