import fluxgui.settings as settings
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class RedshiftTab:
    def __init__(self, window, controllers, settings, connect_widget):
        self.window = window
        self.settings = settings
        self.redshift_controller = controllers["redshift"]
        self.xflux_controller = controllers["xflux"]
        self.latsetting = connect_widget("entryLatitude2",
                                         self.delete_event)
        self.lonsetting = connect_widget("entryLongitude2",
                                         self.delete_event)
        self.colsetting = connect_widget("comboColor2")
        self.previewbutton = connect_widget("buttonPreview2",
                                            self.preview_click_event, "clicked")
        self.closebutton = connect_widget("buttonClose2",
                                          self.delete_event, "clicked")
        self.autostart = connect_widget("checkAutostart2")
        self.checkRedshift = connect_widget("checkRedshift", self._activate_redshift, "toggled")

    def _activate_redshift(self, *args):
        # args[0] is the gtkCheckButton object
        self.settings.use_redshift = args[0].get_active()
        self.settings.use_xflux = not args[0].get_active()

        if self.settings.use_redshift and \
           self.redshift_controller.state != self.redshift_controller.states["RUNNING"]:
            self.xflux_controller.stop()
            self.redshift_controller.state = self.redshift_controller.states["INIT"]
            self.redshift_controller.start()

    def show(self):
        self.latsetting.set_text(self.settings.latitude)
        self.lonsetting.set_text(self.settings.longitude)
        self.colsetting.set_active(settings.temperature_to_key(self.settings.color))

        self.checkRedshift.set_active(self.settings.use_redshift)
        self.autostart.set_active(self.settings.autostart)

    def preview_click_event(self, widget, data=None):
        colsetting_temperature = settings.key_to_temperature(
            self.colsetting.get_active())
        self.redshift_controller.preview_color(colsetting_temperature)

    def save_changes(self):
        if self.settings.latitude != self.latsetting.get_text():
            self.redshift_controller.set_redshift_latitude(
                self.latsetting.get_text())

        if self.settings.longitude != self.lonsetting.get_text():
            self.redshift_controller.set_redshift_longitude(
                self.lonsetting.get_text())

        colsetting_temperature = settings.key_to_temperature(
            self.colsetting.get_active())
        if self.settings.color != colsetting_temperature:
            self.redshift_controller.color = colsetting_temperature

        self.redshift_controller.set_autostart(self.autostart.get_active())

        if self.redshift_controller.new_settings:
            self.redshift_controller.start()
            self.redshift_controller.new_settings.clear()

    def is_latitude_or_longitude_set(self):
        return self.latsetting.get_text() or self.lonsetting.get_text()

    def delete_event(self, widget, data=None):
        if not self.is_latitude_or_longitude_set():
            self.display_no_longitude_or_latitude_error_box()
            return True

        self.save_changes()
        self.window.hide()
        return True

    def display_no_longitude_or_latitude_error_box(self):
        md = gtk.MessageDialog(self.window,
                               gtk.DialogFlags.DESTROY_WITH_PARENT, gtk.MessageType.INFO,
                               gtk.ButtonsType.OK, ("The f.lux indicator applet needs to know "
                                                    "your latitude and longitude to run. "
                                                    "Please fill either of them in on "
                                                    "the preferences screen and click 'Close'."))
        md.set_title("f.lux indicator applet")
        md.run()
        md.destroy()
