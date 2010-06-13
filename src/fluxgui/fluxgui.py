#!/usr/bin/python
import appindicator
import gobject
import gtk
import pynotify
import os
import sys


class Fluxgui:

  def __init__(self):

    self.setup_indicator()

  def setup_indicator(self):
    self.indicator = appindicator.Indicator(
      "fluxgui-indicator",
      "fluxgui",
      appindicator.CATEGORY_APPLICATION_STATUS)
    self.indicator.set_status(appindicator.STATUS_ACTIVE)

    # Check for special Ubuntu themes. copied from lookit
    theme = gtk.gdk.screen_get_default().get_setting(
            'gtk-icon-theme-name')
    if theme == 'ubuntu-mono-dark':
      self.indicator.set_icon('fluxgui-dark')
    elif theme == 'ubuntu-mono-light':
      self.indicator.set_icon('fluxgui-light')
    else:
      self.indicator.set_icon('fluxgui')

    self.indicator.set_menu(self.setup_menu())

  def setup_menu(self):
    menu = gtk.Menu()

    item = gtk.MenuItem("Toggle off")
    item.connect("activate", self.kill_xflux)
    item.show()
    menu.append(item)

    item = gtk.MenuItem("Preferences")
    item.connect("activate", self.open_preferences)
    item.show()
    menu.append(item)

    item = gtk.SeparatorMenuItem()
    item.show()
    menu.append(item)

    item = gtk.MenuItem("Exit")
    item.connect("activate", self.exit)
    item.show()
    menu.append(item)

    return menu

  def start_xflux(self):
    print "start xflux"
    return

  def kill_xflux(self):
    print "kill xflux"
    return

  def open_preferences(self):
    print "open settings"
    return

  def run(self):
    gtk.main()

  def exit(self, widget, data=None):
    gtk.main_quit()
    sys.exit(0)

if __name__=="__main__":
  app = Fluxgui()
  app.run()

