#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* IRM 20/03/2019
* Inicio de aplicación para desarrollo
"""

import gi
import sys, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from src.dialog import winDialog
from src.globfile import xml_use

class builder(Gtk.Builder):
  """docstring for Builder"""
  def __init__(self, **args):
    super().__init__()
    str_builder = xml_use(args["str"])
    if ("str" in args):
      if (str_builder is None):
        print("El directorio no existe...")
      else:
        self.add_from_file("{0}".format(str_builder))
    else:
      self.add_from_string(args["string"])

class widgets(object):
  """docstring for widgets_use"""
  def __init__(self, builder):
    self.builder = builder

  def entry(self, **args):
    entry = None
    try:
      if ("nombre" in args and self.builder is not None):
        entry = self.builder.get_object(args["nombre"])
      elif("new" in args):
        if(args["new"]):
          entry = Gtk.Entry()
      if (entry is not None):
        self.set_entry(entry, **args)
    except Exception as e:
      print("Error: {0}".format(e))
    finally:
      return entry

  def set_entry(self, entry, **args):
    try:
      for key, value in args.items():
        if (key == "evento"):
          value["widget"] = value["widget"] if "widget" in value else None
          entry.connect(value["tipo"], value["funcion"], value["widget"])
        elif (key == "focus"):
          entry.has_focus()
        elif (key == "sensitive"):
          entry.set_sensitive(value)
        elif (key == "set"):
          entry.set_text(value)
    except Exception as e:
      print("Error: {0}".format(e))
  
  # IRM 20/04/2019 Función para menasjes del sistema a mostra; estos mensajes podran ser interactivos botones OK, CANCEL, YES, NO
  def windowsDialog(self, **args):
    try:
      f_ok = args["func_ok"]   if "func_ok" in args else None
      f_yes = args["func_yes"] if "func_yes" in args else None
      f_no = args["func_no"]   if "func_no" in args else None 
      f_can = args["func_cancel"]   if "func_cancel" in args else None 
      _kwargs = args["kwargs"]   if "kwargs" in args else None
      winDialog(args["tipo"].lower(), args["tituloDialog"], args["textDialog"], 
                func_ok=f_ok, func_cancel=f_can, func_yes=f_yes, func_no=f_no, kwargs=_kwargs)
    except Exception as e:
      print("Error: {0}".format(e))
