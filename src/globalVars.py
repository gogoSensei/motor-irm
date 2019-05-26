#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* IRM 20/03/2019
* Inicio de aplicación para desarrollo
"""

import os.path as p
from os import environ as e

global myList

myList = {"dns"  : '',
          "conn" : False,
          "operacion": "" if (e["TIPOOPERACION"]).lower() == "develop" else "/etc/"}

class Metods:
  @staticmethod
  def xmlUse(xml):
    return myList["operacion"]+ "gld/" + xml if p.exists(myList["operacion"]+ "gld/" + xml) else None

  @staticmethod
  def setVar(key, val):
    myList[key] = val

  @staticmethod
  def getVar(key):
    return myList[key] if key in myList else None
