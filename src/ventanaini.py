#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* IRM 20/03/2019
* Inicio de aplicación para desarrollo
"""
import sys, os, gi, threading

# IRM 20/03/2019 Agreagando requerimientos
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk
from src.wgts import Widgets
from src.notify import db
from src.globalVars import Metods

# This would typically be its own file
# Esto debe cambiar para elegir desde donde debe tomar las vistas
MENU_XML = "login.glade"
db = db()

class AppWindow(Gtk.ApplicationWindow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # This will be in the windows group and have the "win" prefix
    builder = Widgets(gld=MENU_XML)
    self.add_child(builder, builder.get_object('box1'), None)
    if (kwargs["application"].usuario is not None):
      euser = builder.entry(nombre="e_usuario", set=kwargs["application"].usuario, )

class Application(Gtk.Application):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, application_id="org.example.myapp", 
                     flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE, **kwargs)
    self.window = None
    self.usuario = None
    self.add_main_option("usuario", ord("u"), GLib.OptionFlags.NONE,
                         GLib.OptionArg.STRING, "Comando para agregar usuario default", None)
  
  def do_activate(self):
    # We only allow a single window and raise any existing ones
    if not self.window:
        # Windows are associated with the application
        # when the last one is closed the application shuts down
        self.window = AppWindow(application=self, title="Main Window")
    self.window.present()
  
  def do_command_line(self, command_line):
    options = command_line.get_options_dict()
    # convert GVariantDict -> GVariant -> dict
    options = options.end().unpack()
    # This is printed on the main instance
    if ("usuario" in options):
      self.usuario = options["usuario"]
    self.activate()
    return 0

class runApp:
  """docstring for runApp"""
  @classmethod
  def win(cls, args):
    app = Application()
    win_run = threading.Thread(target=app.run, args=(args,))
    win_run.start()
