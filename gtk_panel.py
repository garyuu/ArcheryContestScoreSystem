'''
Author: Garyuu
Date:   2016/8/14
Name:   console
Descr.: Simple terminal for user.
'''
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from controller import Controller as controller

class PanelWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self, title="NCTU Archery - Scoring System Control Panel")


