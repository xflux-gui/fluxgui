#!/usr/bin/python

import signal
import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk as gtk
from fluxgui import fluxcontroller, settings
from fluxgui.exceptions import MethodUnavailableError


class FluxGUI(object):
    """
    FluxGUI initializes/destroys the app
    """

    def __init__(self):
        try:
            self.settings = settings.Settings()
            self.xflux_controller = fluxcontroller.FluxController(self.settings)
            self.indicator = Indicator(self, self.xflux_controller)
            self.preferences = Preferences(self.settings,
                                           self.xflux_controller)
            self.xflux_controller.start()

        except Exception as e:
            print(e)
            print("Critical error. Exiting.")
            self.exit(1)

    def __del__(self):
        self.exit()

    def open_preferences(self):
        self.preferences.show()

    def signal_exit(self, signum, frame):
        print('Received signal: ', signum)
        print('Quitting...')
        self.exit()

    def exit(self, code=0):
        try:
            self.xflux_controller.stop()
        except MethodUnavailableError:
            pass
        gtk.main_quit()
        sys.exit(code)

    def run(self):
        gtk.main()


class Indicator(object):
    """
    Information and methods related to the indicator applet.
    Executes FluxController and FluxGUI methods.
    """

    def __init__(self, fluxgui, xflux_controller):
        self.fluxgui = fluxgui
        self.xflux_controller = xflux_controller
        self.indicator = appindicator.Indicator.new(
            "fluxgui-indicator",
            "fluxgui",
            appindicator.IndicatorCategory.APPLICATION_STATUS)

        self.setup_indicator()

    def setup_indicator(self):
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_icon('fluxgui-panel')
        self.indicator.set_menu(self.create_menu())

    def create_menu(self):
        menu = gtk.Menu()

        self.add_menu_item("_Pause f.lux", self._toggle_pause,
                           menu, MenuItem=gtk.CheckMenuItem)
        self.add_menu_item("Prefere_nces", self._open_preferences, menu)
        self.add_menu_separator(menu)
        self.add_menu_item("Quit", self._quit, menu)

        return menu

    def add_menu_item(self, label, handler, menu,
                      event="activate", MenuItem=gtk.MenuItem, show=True):
        item = MenuItem(label)
        item.connect(event, handler)
        menu.append(item)
        if show:
            item.show()
        return item

    def add_menu_separator(self, menu, show=True):
        item = gtk.SeparatorMenuItem()
        menu.append(item)
        if show:
            item.show()

    def _toggle_pause(self, item):
        self.xflux_controller.toggle_pause()

    def _open_preferences(self, item):
        self.fluxgui.open_preferences()

    def _quit(self, item):
        self.fluxgui.exit()


class Preferences(object):
    """
    Information and methods related to the preferences window.
    Executes FluxController methods and gets data from Settings.

    """

    def connect_widget(self, widget_name, connect_target=None,
                       connect_event="activate"):
        widget = self.wTree.get_object(widget_name)
        if connect_target:
            widget.connect(connect_event, connect_target)
        return widget

    def __init__(self, settings, xflux_controller):
        self.settings = settings
        self.xflux_controller = xflux_controller

        self.gladefile = os.path.join(os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))), "fluxgui/preferences.glade")
        self.wTree = gtk.Builder.new_from_file(self.gladefile)

        self.window = self.connect_widget("window1", self.delete_event,
                                          connect_event="destroy")
        self.latsetting = self.connect_widget("entryLatitude",
                                              self.delete_event)
        self.lonsetting = self.connect_widget("entryLongitude",
                                              self.delete_event)
        self.zipsetting = self.connect_widget("entryZipcode",
                                              self.delete_event)
        self.colsetting = self.connect_widget("comboColor")
        self.previewbutton = self.connect_widget("buttonPreview",
                                                 self.preview_click_event, "clicked")
        self.closebutton = self.connect_widget("buttonClose",
                                               self.delete_event, "clicked")
        self.autostart = self.connect_widget("checkAutostart")

        if (self.settings.latitude is "" and self.settings.zipcode is "")\
                or not self.settings.has_set_prefs:
            self.show()
            self.display_no_zipcode_or_latitude_error_box()

    def show(self):

        self.latsetting.set_text(self.settings.latitude)
        self.lonsetting.set_text(self.settings.longitude)
        self.zipsetting.set_text(self.settings.zipcode)
        self.colsetting.set_active(settings.temperature_to_key(self.settings.color))

        if self.settings.autostart:
            self.autostart.set_active(True)
        else:
            self.autostart.set_active(False)

        self.window.show()

    def display_no_zipcode_or_latitude_error_box(self):
        md = gtk.MessageDialog(self.window,
                               gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                               gtk.BUTTONS_OK, ("The f.lux indicator applet needs to know "
                                                "your latitude or zipcode to run. "
                                                "Please fill either of them in on "
                                                "the preferences screen and click 'Close'."))
        md.set_title("f.lux indicator applet")
        md.run()
        md.destroy()

    def preview_click_event(self, widget, data=None):
        colsetting_temperature = settings.key_to_temperature(
            self.colsetting.get_active())
        self.xflux_controller.preview_color(colsetting_temperature)

    def delete_event(self, widget, data=None):
        if self.settings.latitude != self.latsetting.get_text():
            self.xflux_controller.set_xflux_latitude(
                self.latsetting.get_text())

        if self.settings.longitude != self.lonsetting.get_text():
            self.xflux_controller.set_xflux_longitude(
                self.lonsetting.get_text())

        if self.settings.zipcode != self.zipsetting.get_text():
            self.xflux_controller.set_xflux_zipcode(
                self.zipsetting.get_text())

        colsetting_temperature = settings.key_to_temperature(
            self.colsetting.get_active())
        if self.settings.color != colsetting_temperature:
            self.xflux_controller.color = colsetting_temperature

        if self.autostart.get_active():
            self.xflux_controller.set_autostart(True)
        else:
            self.xflux_controller.set_autostart(False)
        if self.latsetting.get_text() == "" \
                and self.zipsetting.get_text() == "":
            self.display_no_zipcode_or_latitude_error_box()
            return True

        self.window.hide()
        return False


def main():
    try:
        app = FluxGUI()
        signal.signal(signal.SIGTERM, app.signal_exit)
        signal.signal(signal.SIGINT, app.signal_exit)
        app.run()
    except KeyboardInterrupt:
        # No idea why we consistently get a keyboard interrupt here
        # after killing fluxgui with SIGINT or SIGTERM ...
        pass


if __name__ == '__main__':
    main()
