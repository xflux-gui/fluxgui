from fluxgui import settings


class XfluxPage:
    def __init__(self, window, xflux_controller, settings, connect_widget):
        self.window = window
        self.settings = settings
        self.xflux_controller = xflux_controller
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
        self.checkXflux = connect_widget("checkXflux", self._switch_to_xflux, "toggled")

    def _switch_to_xflux(self, *args):
        if args[0].get_active():
            self.settings.use_xflux = True
            self.settings.use_redshift = False
        else:
            self.settings.use_xflux = False

    def show(self):
        self.latsetting.set_text(self.settings.latitude)
        self.lonsetting.set_text(self.settings.longitude)
        self.zipsetting.set_text(self.settings.zipcode)
        self.colsetting.set_active(settings.temperature_to_key(self.settings.color))

        if self.settings.use_xflux:
            self.checkXflux.set_active(True)
        else:
            self.checkXflux.set_active(False)

        if self.settings.autostart:
            self.autostart.set_active(True)
        else:
            self.autostart.set_active(False)

    def preview_click_event(self, widget, data=None):
        colsetting_temperature = settings.key_to_temperature(
            self.colsetting.get_active())
        self.xflux_controller.preview_color(colsetting_temperature)

    def delete_event(self, widget, data=None):
        if self.settings.latitude != self.latsetting.get_text():
            self.xflux_controller.set_latitude(
                self.latsetting.get_text())

        if self.settings.longitude != self.lonsetting.get_text():
            self.xflux_controller.set_longitude(
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
        return True
