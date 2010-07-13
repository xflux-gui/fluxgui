#!/usr/bin/python
import appindicator
import gtk
import gtk.glade
import gconf
import sys
import pexpect
from os import path

VERSION = "1.0.0"


class Fluxgui:

    def __init__(self):
        self.indicator = Indicator(self)
        self.settings = Settings(self)

        if self.settings.latitude is "" and self.settings.zipcode is "":
            self.open_preferences("activate")

        self.start_xflux(self.settings.latitude, self.settings.longitude,
                         self.settings.zipcode, self.settings.color)

    def start_xflux(self, latitude, longitude, zipcode, color):
        args = ["-z", zipcode, "-k", color, '-nofork']
        if self.settings.latitude:
            args = ["-l", latitude, "-g", longitude, "-k", color, '-nofork']

        self.xflux = pexpect.spawn("xflux", args)

    def stop_xflux(self, item):
        self.indicator.item_turn_off.hide()
        self.indicator.item_turn_on.show()

        self.xflux.terminate(force=True)

    def pause_xflux(self, item):
        self.indicator.item_turn_off.hide()
        self.indicator.item_turn_on.show()
        self.update_xflux("k=" + self.settings.get_color("4"))

    def unpause_xflux(self, item):
        self.indicator.item_turn_off.show()
        self.indicator.item_turn_on.hide()
        self.update_xflux("k=" + self.settings.color)

    def update_xflux(self, command):
        self.xflux.sendline(command)

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

        self.item_turn_off = gtk.MenuItem("_Pause f.lux")
        self.item_turn_off.connect("activate", self.main.pause_xflux)
        self.item_turn_off.show()
        menu.append(self.item_turn_off)

        self.item_turn_on = gtk.MenuItem("_Unpause f.lux")
        self.item_turn_on.connect("activate", self.main.unpause_xflux)
        self.item_turn_on.hide()
        menu.append(self.item_turn_on)

        item = gtk.MenuItem("_Preferences")
        item.connect("activate", self.main.open_preferences)
        item.show()
        menu.append(item)

        item = gtk.SeparatorMenuItem()
        item.show()
        menu.append(item)

        item = gtk.MenuItem("Quit")
        item.connect("activate", self.main.exit)
        item.show()
        menu.append(item)

        return menu

    def main(self):
        gtk.main()


class Preferences:

    def __init__(self, main):
        self.main = main
        self.gladefile = path.join(path.dirname(path.dirname(
          path.realpath(__file__))), "fluxgui/preferences.glade")
        self.wTree = gtk.glade.XML(self.gladefile)

        self.window = self.wTree.get_widget("window1")
        self.window.connect("destroy", self.delete_event)

        self.latsetting = self.wTree.get_widget("entry1")
        self.latsetting.set_text(self.main.settings.latitude)
        self.latsetting.connect("activate", self.delete_event)

        self.lonsetting = self.wTree.get_widget("entry3")
        self.lonsetting.set_text(self.main.settings.longitude)
        self.lonsetting.connect("activate", self.delete_event)

        self.zipsetting = self.wTree.get_widget("entry2")
        self.zipsetting.set_text(self.main.settings.zipcode)
        self.zipsetting.connect("activate", self.delete_event)

        self.colsetting = self.wTree.get_widget("combobox1")
        self.colsetting.set_active(int(self.main.settings.colortemp))

        if self.main.settings.latitude is ""\
           and self.main.settings.zipcode is "":
            md = gtk.MessageDialog(self.window,
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                gtk.BUTTONS_OK, "The f.lux indicator applet needs to know " +
                "your latitude and longitude or zipcode to work correctly. " +
        "Please fill either of them in on the next screen and then hit enter.")
            md.set_title("f.lux indicator applet")
            md.run()
            md.destroy()
            self.window.show()
        else:
            self.window.show()

    def delete_event(self, widget, data=None):
        if self.main.settings.latitude != self.latsetting.get_text():
            self.main.settings.set_latitude(self.latsetting.get_text())

        if self.main.settings.longitude != self.lonsetting.get_text():
            self.main.settings.set_longitude(self.lonsetting.get_text())

        if self.main.settings.zipcode != self.zipsetting.get_text():
            self.main.settings.set_zipcode(self.zipsetting.get_text())

        if self.main.settings.colortemp != str(self.colsetting.get_active()):
            self.main.settings.set_colortemp(str(self.colsetting.get_active()))

        self.window.hide()
        return False

    def main(self):
        gtk.main()


class Settings:

    def __init__(self, main):
        self.main = main
        self.client = gconf.client_get_default()
        self.prefs_key = "/apps/fluxgui"
        self.client.add_dir(self.prefs_key, gconf.CLIENT_PRELOAD_NONE)

        self.latitude = self.client.get_string(self.prefs_key + "/latitude")
        self.longitude = self.client.get_string(self.prefs_key + "/longitude")
        self.zipcode = self.client.get_string(self.prefs_key + "/zipcode")
        self.colortemp = self.client.get_string(self.prefs_key + "/colortemp")
        self.color = self.get_color(self.colortemp)

        if self.latitude is None:
            self.latitude = ""

        if self.longitude is None:
            self.longitude = ""

        if self.zipcode is None:
            self.zipcode = ""

        if not self.colortemp:
            self.colortemp = "1"

    def set_latitude(self, latitude):
        self.client.set_string(self.prefs_key + "/latitude", latitude)
        self.latitude = latitude

        command = "l=" + latitude
        self.main.update_xflux(command)

    def set_longitude(self, longitude):
        self.client.set_string(self.prefs_key + "/longitude", longitude)
        self.longitude = longitude

        command = "g=" + longitude
        self.main.update_xflux(command)

    def set_zipcode(self, zipcode):
        self.client.set_string(self.prefs_key + "/zipcode", zipcode)
        self.zipcode = zipcode

        command = "z=" + zipcode
        self.main.update_xflux(command)

    def get_color(self, colortemp):
        color = "3400"
        if colortemp is "0":
            #tungsten
            color = "2700"
        elif colortemp is "1":
            #halogen
            color = "3400"
        elif colortemp is "2":
            #fluorescent
            color = "4200"
        elif colortemp is "3":
            #daylight
            color = "5000"
        elif colortemp is "4":
            #off
            color = "6500"

        return color

    def set_colortemp(self, colortemp):
        color = self.get_color(colortemp)

        self.client.set_string(self.prefs_key + "/colortemp", colortemp)
        self.colortemp = colortemp
        self.color = color

        command = "k=" + color
        self.main.update_xflux(command)

    def main(self):
        gtk.main()


if __name__ == "__main__":
    app = Fluxgui()
    app.run()

