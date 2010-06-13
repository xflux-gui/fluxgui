#!/usr/bin/python
import appindicator
import gtk
import sys
import subprocess

class Fluxgui:

  def __init__(self):
    self.indicator = Indicator(self)
    self.start_xflux("52.07") #get these from preferences file

  def start_xflux(self, latitude):
    self.xflux = subprocess.Popen(["/bin/xflux", "-l", latitude], stdout=subprocess.PIPE)

    returncode = self.xflux.stdout
    self.xfluxKillCode = ""

    while True:
      line = returncode.readline()
      if "background" in line:
        newline = line.split("\'")
        self.xfluxKillCode = newline[1]
        return
      return

  def kill_xflux(self, item):
    self.indicator.killxflux.hide()
    self.indicator.restartxflux.show()

    self.xfluxKill = subprocess.Popen(self.xfluxKillCode, stdout=subprocess.PIPE)

  def restart_xflux(self, item):
    self.indicator.killxflux.show()
    self.indicator.restartxflux.hide()

    self.start_xflux("52.07") #get these from preferences file

  def open_preferences(self, item):
    print "yellow"
    self.preferences = Preferences(self)

  def run(self):
    gtk.main()

  def exit(self, widget, data=None):
    self.kill_xflux("activate")
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

    self.killxflux = gtk.MenuItem("_Turn f.lux off")
    self.killxflux.connect("activate", self.main.kill_xflux)
    self.killxflux.show()
    menu.append(self.killxflux)

    self.restartxflux = gtk.MenuItem("_Turn f.lux on")
    self.restartxflux.connect("activate", self.main.restart_xflux)
    self.restartxflux.hide()
    menu.append(self.restartxflux)

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
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_title("fluxgui preferences")
    self.window.connect("delete_event", self.delete_event)
    self.window.set_border_width(10)

    self.button = gtk.Button("Hello World")
    #self.button.connect("clicked", self.hello, None)
    self.window.add(self.button)

    self.button.show()

    self.window.show()

  def delete_event(self, widget, data=None):
    print "save stuff here"
    return False

  def main(self):
    gtk.main()

if __name__=="__main__":
  app = Fluxgui()
  app.run()

