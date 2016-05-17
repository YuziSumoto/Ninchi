# -*- coding: UTF-8 -*-

import datetime # 日付モジュール

def CheckDate(self,Hizuke): # 日付チェック

  if Hizuke == "":
    return True

  ErrFlg = False

  try:
      newDate=datetime.datetime.strptime(Hizuke,"%Y/%m/%d")
      return True # 西暦入力ならここで終了
  except ValueError:
      ErrFlg = False

  Hizuke = Hizuke.replace(".","/") # 年月日区切り変更

  if   Hizuke[0:1] == "M" or Hizuke[0:1] == "m": # 明治
    Nensu =  1867
  elif Hizuke[0:1] == "T" or Hizuke[0:1] == "t" : # 大正
    Nensu =  1911
  elif Hizuke[0:1] == "S" or Hizuke[0:1] == "s": # 昭和
    Nensu =  1925
  elif Hizuke[0:1] == "H" or Hizuke[0:1] == "h": # 平成
    Nensu = 1988
  else:
    return False  # 元号異常入力ならここで終了

  Counter = 0
  for Mozi in Hizuke:
    if Mozi == "/":
      Counter += 1
  if Counter != 2:
    return False  # /が２つ以外ならここで終了

  Nen,Tuki,Hi = Hizuke[1:10].split("/")   # 元号外して区切る
  if Nen == "" or Tuki == "" or Hi == "":
    return False # 元号異常入力ならここで終了
  if Nen.isdigit() == False or Tuki.isdigit() == False or Hi.isdigit() == False:
    return False  # 元号異常入力ならここで終了

  Nen = int(Nen) + Nensu

  try:
      Hizuke = str(Nen) + "/" + str(Tuki) + "/" + str(Hi) 
      newDate=datetime.datetime.strptime(Hizuke,"%Y/%m/%d")
      return True  # 和歴入力ならここで終了
  except ValueError:
      return False

def WarekiHenkan(self,Hizuke): # 和歴→西暦

  if Hizuke == "":
    return None
    
  try:
      Seireki  = datetime.datetime.strptime(Hizuke,"%Y/%m/%d")
      return Seireki # 西暦入力ならここで終了
  except ValueError:
      ErrFlg = False

  Hizuke = Hizuke.replace(".","/") # 年月日区切り変更

  if Hizuke[0:1] == "M" or Hizuke[0:1] == "m": # 明治
    Nensu =  1867
  elif Hizuke[0:1] == "T" or Hizuke[0:1] == "t": # 大正
    Nensu =  1911
  elif Hizuke[0:1] == "S" or Hizuke[0:1] == "s": # 昭和
    Nensu =  1925
  elif Hizuke[0:1] == "H" or Hizuke[0:1] == "h": # 平成
    Nensu = 1988
  else:
    return None  # 元号異常入力ならここで終了

  Nen,Tuki,Hi = Hizuke[1:10].split("/")   # 元号外して区切る
  Nen = int(Nen) + Nensu

  try:
      Hizuke = str(Nen) + "/" + str(Tuki) + "/" + str(Hi) 
      Seireki = datetime.datetime.strptime(Hizuke,"%Y/%m/%d")
      return Seireki  # 和歴入力ならここで終了
  except ValueError:
      return None


def CheckTime(self,Zikoku): # 時刻チェック

  if Zikoku == "":
    return True

  try:
      newDate=datetime.datetime.strptime(Zikoku,"%H:%M")
      return True
  except ValueError:
      return False

def GetWareki(Hizuke): # 和歴取得
  
  if Hizuke == "" or Hizuke is None:
    return ""
  
  if    Hizuke < datetime.datetime.strptime('1912/07/30', '%Y/%m/%d'):  # 明治
    Gango = "M"
    Nensu = Hizuke.year - 1867
  elif  Hizuke < datetime.datetime.strptime('1926/12/25', '%Y/%m/%d'):  # 大正
    Gango = "T"
    Nensu = Hizuke.year - 1911
  elif  Hizuke < datetime.datetime.strptime('1989/01/08', '%Y/%m/%d'): # 昭和
    Gango = "S"
    Nensu = Hizuke.year - 1925
  else:                      # 平成
    Gango = "H"
    Nensu = Hizuke.year - 1988

  return Gango + str(Nensu) + "." + Hizuke.strftime("%m.%d")

