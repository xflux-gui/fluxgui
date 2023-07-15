#!/usr/bin/env python3

import signal
import os
import sys
import fluxgui.settings as settings
from fluxgui.settings.xflux import XfluxSettings
from fluxgui.settings.redshift import RedshiftSettings
from fluxgui.tabs.xflux import XfluxTab
from fluxgui.tabs.redshift import RedshiftTab
from fluxgui.exceptions import MethodUnavailableError

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
# As of 2022/03/23 there is no Ayatana appindicator on Fedora, so fall
# back to using regular appindicator if necessary.
try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as appindicator
except:
    print('Failed to import Ayatana appindicator, falling back to plain appindicator ...')
    try:
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import AppIndicator3 as appindicator
    except:
        print('Failed to import plain appindicator ...')
        print('Failed to import an appindicator implementation, dying ...')
        sys.exit(1)

class FluxGUI(object):
    """
    FluxGUI initializes/destroys the app
    """

    def __init__(self):
        try:
            self.settings = settings.Settings()
            self.controllers = {"xflux": XfluxSettings(self.settings),
                                "redshift": RedshiftSettings(self.settings)}
            self.indicator = Indicator(self, self.controllers)

            if self.settings.use_redshift:
                self.controllers["redshift"].start()
            elif self.settings.use_xflux:
                self.controllers["xflux"].start()

            self.preferences = Preferences(self.settings, self.controllers)

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
            if self.settings.use_redshift:
                self.controllers["redshift"].stop()
            elif self.settings.use_xflux:
                self.controllers["xflux"].stop()
        except MethodUnavailableError as e:
            print(e)
        gtk.main_quit()
        sys.exit(code)

    def run(self):
        gtk.main()


class Indicator(object):
    """
    Information and methods related to the indicator applet.
    Executes FluxController and FluxGUI methods.
    """

    def __init__(self, fluxgui, controllers):
        self.fluxgui = fluxgui
        self.xflux_controller = controllers["xflux"]
        self.redshift_controller = controllers["redshift"]
        self.indicator = appindicator.Indicator.new(
            "fluxgui-indicator",
            "fluxgui",
            appindicator.IndicatorCategory.APPLICATION_STATUS)

        self.setup_indicator()

    def setup_indicator(self):
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_icon_full('fluxgui-panel', '')
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
        item = MenuItem(label=label)
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
        if self.fluxgui.settings.use_redshift:
            self.redshift_controller.toggle_pause()
        elif self.fluxgui.settings.use_xflux:
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

    def __init__(self, settings, controllers):
        self.settings = settings

        self.gladefile = os.path.join(os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))), "fluxgui/preferences.glade")
        self.wTree = gtk.Builder.new_from_file(self.gladefile)

        self.window = self.connect_widget("window1", self.delete_event,
                                          connect_event="delete-event")
        self.notebook = self.connect_widget("notebook", self.switch_page,
                                            connect_event="switch-page")
        self.xflux_tab = XfluxTab(self.window, controllers, self.settings,
                                  self.connect_widget)
        self.redshift_tab = RedshiftTab(self.window, controllers, self.settings,
                                        self.connect_widget)

        if not self.settings.has_set_prefs:
            self.show()
            if self.settings.latitude and self.settings.zipcode:
                self.xflux_tab.display_no_zipcode_or_latitude_error_box()
            elif self.settings.latitude and self.settings.longitude:
                self.redshift_tab.display_no_longitude_or_latitude_error_box()

    def connect_widget(self, widget_name, connect_target=None,
                       connect_event="activate"):
        widget = self.wTree.get_object(widget_name)
        if connect_target:
            widget.connect(connect_event, connect_target)
        return widget

    def switch_page(self, *args):
        # the NoteBook page index is the last element of the list
        if args[2] == 0:  # Xflux page
            self.xflux_tab.show()
        elif args[2] == 1:  # Redshift page
            self.redshift_tab.show()

    def delete_event(self, widget, data=None):
        if not self.redshift_tab.are_latitude_and_longitude_set() and self.settings.use_redshift:
            self.redshift_tab.display_no_longitude_or_latitude_error_box()
            return True
        elif not self.xflux_tab.is_latitude_or_zipcode_set() and self.settings.use_xflux:
            self.xflux_tab.display_no_zipcode_or_latitude_error_box()
            return True

        if self.settings.use_redshift:
            self.redshift_tab.save_changes()
        elif self.settings.use_xflux:
            self.xflux_tab.save_changes()

        self.window.hide()
        return True

    def show(self):
        if self.settings.use_xflux:
            self.xflux_tab.show()
            self.notebook.set_current_page(0)
        elif self.settings.use_redshift:
            self.redshift_tab.show()
            self.notebook.set_current_page(1)

        self.window.show()


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
