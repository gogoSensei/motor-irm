#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* IRM 20/03/2019
* Inicio de aplicación para desarrollo
"""

import select
import psycopg2
import psycopg2.extensions as ext
import os
from src.globfile import myList

class db(object):
  def notify(self):
    try:
      with psycopg2.connect(myList["dns"]) as conn:
        conn.set_isolation_level(ext.ISOLATION_LEVEL_AUTOCOMMIT)
        
        curs = conn.cursor()
        if (curs is None):
          print("Error de conexion.")
          return
        for _notify in ['test', 'signal']:
          try:
            curs.execute("LISTEN {0};".format(_notify))
          except psycopg2.Error as e:
            print("{0}: {1}".format(e.diag.severity, e.diag.message_primary))
        print("Waiting for notifications on channel 'test', 'signal'")
        
        while 1:
          if not (select.select([conn],[],[],5) == ([],[],[])):
            conn.poll()
            while conn.notifies:
              notify = conn.notifies.pop(0)
              print ("Got NOTIFY:", notify.pid, notify.channel, notify.payload)
          if (not myList["conn"]):
            conn.close()
            break
    except psycopg2.Error as e:
      print('{0} : {1}'.format(e.diag.severity, e.diag.message_primary))
  
  def query_slt(self, query, *params):
    try:
      with connect(myList["dns"]) as conn:
        conn.set_session(readonly=True, autocommit=True)
        with conn.cursor() as curs:
          curs.execute("SELECT pre-request('{0}', '{1}')".format(myList["user"], myList["pass"]))
          if (params is None):
            curs.execute(query)
          else:
            curs.execute(query, params)
          _res = curs.fetchall()
    except psycopg2.Error as e:
      _res = (e.diag.severity, e.diag.message_primary)
    finally:
      conn.close()
      return _res
