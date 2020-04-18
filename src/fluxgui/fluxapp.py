#!/usr/bin/env python3

from fluxgui.exceptions import MethodUnavailableError
from fluxgui import fluxcontroller, settings
from fluxgui.redshiftcontroller import RedshiftSettings
from fluxgui.xfluxpage import XfluxPage
from fluxgui.redshiftpage import RedshiftPage
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
import signal
import os
import sys


class FluxGUI(object):
    """
    FluxGUI initializes/destroys the app
    """
    def __init__(self):
        try:
            self.settings = settings.Settings()
            self.xflux_controller = fluxcontroller.FluxController(self.settings)
            self.redshift_controller = RedshiftSettings(self.settings)
            self.indicator = Indicator(self, self.xflux_controller)
            self.preferences = Preferences(self.settings,
                    self.xflux_controller, self.redshift_controller)
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

        self.add_menu_item("Pause f.lux", self._toggle_pause,
                menu, MenuItem=gtk.CheckMenuItem)
        self.add_menu_item("Preferences", self._open_preferences, menu)
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

    def switch_page(self, *args):
        # the NoteBook page index is the last element of the list
        if args[2] == 0:  # Xflux page
            self.xflux_page.show()
        elif args[2] == 1:  # Redshift page
            self.redshift_page.show()

    def __init__(self, settings, xflux_controller, redshift_controller):
        self.settings = settings
        # self.xflux_controller = xflux_controller

        self.gladefile = os.path.join(os.path.dirname(os.path.dirname(
          os.path.realpath(__file__))), "fluxgui/preferences.glade")
        self.wTree = gtk.Builder.new_from_file(self.gladefile)

        # self.window = self.connect_widget("window1", self.delete_event,
        self.window = self.connect_widget("window1", gtk.main_quit,
                connect_event="delete-event")
        self.notebook = self.connect_widget("notebook", self.switch_page,
                                            connect_event="switch-page")
        self.xflux_page = XfluxPage(self.window, xflux_controller, self.settings,
                                    self.connect_widget)
        self.redshift_page = RedshiftPage(self.window, redshift_controller, self.settings,
                                          self.connect_widget)
        self.default_page = self.xflux_page

        if (self.settings.latitude == "" and self.settings.zipcode == "")\
                or not self.settings.has_set_prefs:
            self.show()
            self.display_no_zipcode_or_latitude_error_box()

    def show(self):
        self.default_page.show()
        self.window.show()

    def display_no_zipcode_or_latitude_error_box(self):
        md = gtk.MessageDialog(self.window,
                gtk.DialogFlags.DESTROY_WITH_PARENT, gtk.MessageType.INFO,
                gtk.ButtonsType.OK, ("The f.lux indicator applet needs to know "
                "your latitude or zipcode to run. "
                "Please fill either of them in on "
                "the preferences screen and click 'Close'."))
        md.set_title("f.lux indicator applet")
        md.run()
        md.destroy()

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
