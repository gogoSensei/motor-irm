#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# IRM 20/04/2019: Ventana de mensajes interactivas

import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class winDialog(Gtk.Window):
  """Ventana emergente para vsualizar mensajes del sistema"""
  def __init__(self, tipo=None, tituloDialog='', textDialog='', func_ok=None, func_cancel=None, 
               func_yes=None, func_no=None, **kwargs):
    super().__init__(title='Sin titulo')
    dTipo = None
    dButton = None

    # IRM: Selección de tipo de mensajes asi como tipo de botones 
    if (tipo == 'info'):
      dTipo = Gtk.MessageType.INFO
      dButton = Gtk.ButtonsType.OK
    elif (tipo == 'error'):
      dTipo = Gtk.MessageType.ERROR
      dButton = Gtk.ButtonsType.CANCEL
    elif (tipo == 'warning'):
      dTipo = Gtk.MessageType.WARNING
      dButton = Gtk.ButtonsType.OK_CANCEL
    elif (tipo == 'question'):
      dTipo = Gtk.MessageType.QUESTION
      dButton = Gtk.ButtonsType.YES_NO
    else:
      return

    # IRM Creación de ventana para dialogo
    dialog = Gtk.MessageDialog(self, 0, dTipo, dButton, tituloDialog)
    dialog.format_secondary_text(textDialog)
    response = dialog.run()

    # IRM: Acción posterior a respuesta
    try:
      if (response == Gtk.ResponseType.OK and func_ok is not None):
        func_ok(**(kwargs["kwargs"]))
      elif ((response == Gtk.ResponseType.CANCEL or response == Gtk.ResponseType.DELETE_EVENT) and 
             func_cancel is not None):
        func_cancel(**(kwargs["kwargs"]))
      elif (response == Gtk.ResponseType.YES and func_yes is not None):
        func_yes(**(kwargs["kwargs"]))
      elif((response == Gtk.ResponseType.NO or response == Gtk.ResponseType.DELETE_EVENT) and 
             func_no is not None):
        func_no(**(kwargs["kwargs"]))
    except Exception as e:
      print("Error: {0}".format(e))
    dialog.destroy()
