import fluxgui.settings as settings
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk


class XfluxTab:
    def __init__(self, window, controllers, settings, connect_widget):
        self.window = window
        self.settings = settings
        self.xflux_controller = controllers["xflux"]
        self.redshift_controller = controllers["redshift"]
        self.latsetting = connect_widget("entryLatitude1",
                                         self.delete_event)
        self.lonsetting = connect_widget("entryLongitude1",
                                         self.delete_event)
        self.zipsetting = connect_widget("entryZipcode1",
                                         self.delete_event)
        self.colsetting = connect_widget("comboColor1")
        self.previewbutton = connect_widget("buttonPreview1",
                                            self.preview_click_event, "clicked")
        self.closebutton = connect_widget("buttonClose1",
                                          self.delete_event, "clicked")
        self.autostart = connect_widget("checkAutostart1")
        self.checkXflux = connect_widget("checkXflux", self._activate_xflux, "toggled")

    def _activate_xflux(self, *args):
        # args[0] is the gtkCheckButton object
        self.settings.use_xflux = args[0].get_active()
        self.settings.use_redshift = not args[0].get_active()
        if self.settings.use_xflux and \
           self.xflux_controller.state != self.xflux_controller.states["RUNNING"]:
            self.redshift_controller.stop()
            self.xflux_controller.state = self.xflux_controller.states["INIT"]
            self.xflux_controller.start()

    def show(self):
        self.latsetting.set_text(self.settings.latitude)
        self.lonsetting.set_text(self.settings.longitude)
        self.zipsetting.set_text(self.settings.zipcode)
        self.colsetting.set_active(settings.temperature_to_key(self.settings.color))

        self.checkXflux.set_active(self.settings.use_xflux)
        self.autostart.set_active(self.settings.autostart)

    def preview_click_event(self, widget, data=None):
        colsetting_temperature = settings.key_to_temperature(
            self.colsetting.get_active())
        self.xflux_controller.preview_color(colsetting_temperature)

    def save_changes(self):
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

        self.xflux_controller.set_autostart(self.autostart.get_active())

    def is_latitude_or_zipcode_set(self):
        return self.latsetting.get_text() or self.zipsetting.get_text()

    def delete_event(self, widget, data=None):
        if not self.is_latitude_or_zipcode_set():
            self.display_no_zipcode_or_latitude_error_box()
            return True

        self.save_changes()
        self.window.hide()
        return True

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
