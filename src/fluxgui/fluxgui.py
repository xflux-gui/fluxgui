#!/usr/bin/python
import appindicator
import gtk
import gtk.glade
import sys
import subprocess

VERSION = "1.0.0"
MYLATITUDE = "52.07"

class Fluxgui:

  def __init__(self):
    self.indicator = Indicator(self)
    self.start_xflux(MYLATITUDE) #get these from preferences file

  def start_xflux(self, latitude):
    process = subprocess.Popen(["/bin/xflux", "-l", latitude], stdout=subprocess.PIPE)

    returncode = process.stdout
    self.xflux_kill_code = ""

    #figure out if this is correct
    while True:
      line = returncode.readline()
      if "background" in line:
        newline = line.split("\'")
        self.xflux_kill_code = newline[1]
        return
      return

  def stop_xflux(self, item):
    self.indicator.item_turn_off.hide()
    self.indicator.item_turn_on.show()

    #figure out how to get this actually working (permission denied, now)
    process = subprocess.Popen(self.xflux_kill_code, stdout=subprocess.PIPE)

  def restart_xflux(self, item):
    self.stop_xflux(self, "activate")

    self.indicator.item_turn_off.show()
    self.indicator.item_turn_on.hide()

    self.start_xflux(MYLATITUDE) #get these from preferences file

  def open_preferences(self, item):
    self.preferences = Preferences(self)

  def run(self):
    gtk.main()

  def exit(self, widget, data=None):
    self.stop_xflux("activate")
    gtk.main_quit()
    sys.exit(0)


class Indicator:

  def __init__(self, main):
    self.main = main
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

    self.item_turn_off = gtk.MenuItem("_Turn f.lux off")
    self.item_turn_off.connect("activate", self.main.stop_xflux)
    self.item_turn_off.show()
    menu.append(self.item_turn_off)

    self.item_turn_on = gtk.MenuItem("_Turn f.lux on")
    self.item_turn_on.connect("activate", self.main.restart_xflux)
    self.item_turn_on.hide()
    menu.append(self.item_turn_on)

    item = gtk.MenuItem("_Preferences")
    item.connect("activate", self.main.open_preferences)
    item.show()
    menu.append(item)

    item = gtk.SeparatorMenuItem()
    item.show()
    menu.append(item)

    item = gtk.MenuItem("Exit")
    item.connect("activate", self.main.exit)
    item.show()
    menu.append(item)

    return menu

  def main(self):
    gtk.main()


class Preferences:

  def __init__(self, main):
    self.gladefile = "preferences.glade"
    self.wTree = gtk.glade.XML(self.gladefile)

    self.window = self.wTree.get_widget("window1")

    self.window.show()

  def delete_event(self, widget, data=None):
    #get latitude and save it
    return False

  def main(self):
    gtk.main()


if __name__=="__main__":
  app = Fluxgui()
  app.run()

