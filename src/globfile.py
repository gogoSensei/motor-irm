#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* IRM 20/03/2019
* Inicio de aplicación para desarrollo
"""

import os.path as p

global myList

myList = {"dns"  : '',
          "conn" : False,
          "operacion": "/etc/"}

def xml_use(xml):
  return myList["operacion"]+ "gld/" + xml if p.exists(myList["operacion"]+ "gld/" + xml) else None
