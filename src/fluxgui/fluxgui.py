#!/usr/bin/python
import appindicator
import gtk
import sys
import subprocess

class Fluxgui:

  def __init__(self):

    self.setup_indicator()
    self.start_xflux("52.07", "4.51") #get these from preferences file

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

    self.killxflux = gtk.MenuItem("_Turn f.lux off")
    self.killxflux.connect("activate", self.kill_xflux)
    self.killxflux.show()
    menu.append(self.killxflux)

    self.restartxflux = gtk.MenuItem("_Turn f.lux on")
    self.restartxflux.connect("activate", self.restart_xflux)
    self.restartxflux.hide()
    menu.append(self.restartxflux)

    item = gtk.MenuItem("_Preferences")
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

  def start_xflux(self, latitude, longitude):
    runString = ["/bin/xflux", "-l", latitude, longitude]
    self.xflux = subprocess.Popen(runString)

  def restart_xflux(self, item):
    self.killxflux.show()
    self.restartxflux.hide()

    self.start_xflux("52.07", "4.51") #get these from preferences file

  def kill_xflux(self, item):
    self.killxflux.hide()
    self.restartxflux.show()

    self.xflux.terminate()

  def open_preferences(self, item):
    print "open settings"
    return

  def run(self):
    gtk.main()

  def exit(self, widget, data=None):
    self.kill_xflux("activate")
    gtk.main_quit()
    sys.exit(0)

if __name__=="__main__":
  app = Fluxgui()
  app.run()

