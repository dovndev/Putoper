#!/usr/bin/env python3
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
try:
    from auto_typing_gtk import AutoTyperWindow
except ImportError:
    # If running from zipapp where .pyw or .pyc might be used, imports can act differently
    # But usually zipapp adds the archive to sys.path so direct import works.
    from .auto_typing_gtk import AutoTyperWindow

def main():
    win = AutoTyperWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
