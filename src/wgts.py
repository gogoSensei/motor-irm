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
from src.dialog import Dialog
from src.globalVars import Metods

class Widgets(Gtk.Builder):
  """docstring for Builder"""
  def __init__(self, **args):
    super().__init__()
    if ("gld" in args):
      if (Metods.xmlUse(args["gld"]) is None):
        print("El directorio no existe...")
      else:
        self.add_from_file(Metods.xmlUse(args["gld"]))
    elif ("str" in args):
      self.add_from_string(args["str"])

  # IRM 21/04/2019 Propiedades para uso comun, TODO: encontrar un buen uso
  @property
  def builder(self):
    return self
  
  @property
  def wdgts(self):
    return self.__wdgts
  
  @wdgts.setter
  def wdgts(self, new):
    if (new not in self.__wdgts):
      self.__wdgts.append(new)

  def entry(self, **args):
    entry = None
    try:
      if ("nombre" in args and self is not None):
        entry = self.get_object(args["nombre"])
      elif("new" in args):
        if(args["new"]):
          entry = Gtk.Entry()
      if (entry is not None):
        self.set_entry(entry, **args)
    except Exception as e:
      print("Error: {0}".format(e))
    finally:
      return entry

  @classmethod
  def set_entry(cls, entry, **args):
    try:
      # agregando widgets para llevar control; Todavia no pienso bien de que, pero lo haré!!!
      cls.wdgts = entry
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
  @staticmethod
  def windowsDialog(**args):
    try:
      f_ok = args["func_ok"]   if "func_ok" in args else None
      f_yes = args["func_yes"] if "func_yes" in args else None
      f_no = args["func_no"]   if "func_no" in args else None 
      f_can = args["func_cancel"]   if "func_cancel" in args else None 
      _kwargs = args["kwargs"]   if "kwargs" in args else None
      Dialog(args["tipo"].lower(), args["tituloDialog"], args["textDialog"], 
            func_ok=f_ok, func_cancel=f_can, func_yes=f_yes, func_no=f_no, kwargs=_kwargs)
    except Exception as e:
      print("Error: {0}".format(e))

  def button(self, **args):
    button = None
    try:
      if ("nombre" in args and self is not None):
        button = self.get_object(args["nombre"])
      elif("new" in args):
        if(args["new"]):
          button = Gtk.Button()
      if (button is not None):
        self.set_button(button, **args)
    except Exception as e:
      print("Error: {0}".format(e))
    finally:
      return button
  
  @classmethod
  def set_button(cls, button, **args):
    try:
      for key, value in args.items():
        if (key == "evento"):
          value["widgets"] = value["widgets"] if 'widgets' in value else None
          button.connect(value["tipo"], value["funcion"], value["widgets"])
        if (key == "set" and value == "click"):
          button.do_clicked()
    except Exception as e:
      print("Error: {0}".format(e))

  def comboBox(self, **args):
    try:
      cb = args["cb"] if 'cb' in args else self.builder.get_object(args["nombre"])
      if (args["tipo"] == 'cbox'):
        dblist = Gtk.ListStore(str)
        for data in args["lista"]:
          dblist.append([data])
      else:
        dblist = Gtk.ListStore(*args["num_el"])
        dblist.append(*args["lista"])
      cb.set_model(dblist)
      render = Gtk.CellRendererText()
      cb.pack_start(render, True)
      cb.add_attribute(render, 'text', 0)
      for key,value in args.items():
        if (key == 'evento'):
          value["widgets"] = value["widgets"] if 'widgets' in value else None
          cb.connect(value["tipo"], value["funcion"], value["widgets"])
    except Exception as e:
      print(e)
      cb = None
    return cb

  @classmethod
  def getDataCombo(self, combo):
    data = None
    try:
      tree_iter = combo.get_active_iter()
      if tree_iter is not None:
        model = combo.get_model()
        data = model[tree_iter]
    except Exception as e:
      print(e)
    return data
  
  @classmethod
  def get_type_widget(cls, widget):
    try:
      wdgt = widget.__gtype__.name 
    except Exception as e:
      wdgt = ""
    finally:
      return wdgt



"""
Pruebas sobre aspectos de clase

class circulo(object): 
    def __new__(cls): 
        return super().__new__(cls) 
     
    def __init__(self): 
        print("Iniciando clase") 
        self.x = "pruebas" 
     
    def __repr__(self): 
        return("Hola que hace") 
         
    def __str__(self): 
        return("descripción de clase") 
         
    @property 
    def radio(self): 
        return self.__radio 
     
    @radio.setter 
    def radio(self, radio): 
        self.__radio = radio 
     
    @staticmethod 
    def respuesta(x): 
        return("respuesta esta en " + x)

"""