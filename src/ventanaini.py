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
from src.wgts import builder, widgets
from src.notify import db
from src.globfile import myList

# This would typically be its own file
# Esto debe cambiar para elegir desde donde debe tomar las vistas
MENU_XML = "login.glade"
db = db()

class AppWindow(Gtk.ApplicationWindow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # This will be in the windows group and have the "win" prefix
    _builder = builder(str=MENU_XML)
    w = widgets(_builder)
    self.add_child(_builder, _builder.get_object('box1'), None)
    euser = w.entry(nombre="e_usuario", set=kwargs["application"].usuario)


class Application(Gtk.Application):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, application_id="org.example.myapp", 
                     flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE, **kwargs)
    self.window = None
    self.usuario = None
    self.add_main_option("usuario", ord("u"), GLib.OptionFlags.NONE,
                         GLib.OptionArg.STRING, "Comando para agregar usuario default", None)
    self.add_main_option("operacion", ord("o"), GLib.OptionFlags.NONE,
                         GLib.OptionArg.STRING, "Comando para agregar tipo de operacion", None)

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
    if ("operacion" in options):
      if (options["operacion"] == "develop"):
        myList["operacion"] = ''
    # This is printed on the main instance
    if ("usuario" in options):
      self.usuario = options["usuario"]
    self.activate()
    return 0

class runApp:
  """docstring for runApp"""
  def __init__(self, argv):
    self.win_run(argv)
    
  def win(self, args):
    app = Application()
    app.run(args)
    
  def win_run(self, argv):
    #myList["path"] = '/path/to/certfile'
    #myList["dns"] = 'postgres://authenticator:1326011c3c01d5ca57fbb5741673c72d@localhost:5432/motor_test'
    win_run = threading.Thread(target=self.win, args=(argv,))
    #dbconn = threading.Thread(target=db.notify)
    win_run.start()
    #dbconn.start()
