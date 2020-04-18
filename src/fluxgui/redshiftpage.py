from fluxgui import settings


class RedshiftPage:
    def __init__(self, window, redshift_controller, settings, connect_widget):
        self.window = window
        self.settings = settings
        self.redshift_controller = redshift_controller
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
        self.checkRedshift = connect_widget("checkRedshift", self.switch_to_redshift, "toggled")

    def switch_to_redshift(self, *args):
        if args[0].get_active():
            self.settings.use_redshift = True
            self.settings.use_xflux = False
        else:
            self.settings.use_redshift = False

    def show(self):
        self.latsetting.set_text(self.settings.latitude)
        self.lonsetting.set_text(self.settings.longitude)
        self.colsetting.set_active(settings.temperature_to_key(self.settings.color))

        if self.settings.use_redshift:
            self.checkRedshift.set_active(True)
        else:
            self.checkRedshift.set_active(False)

        # if self.checkRedshift.get_active():
            # print(f"use_redshift={self.settings.use_redshift} use_xflux={self.settings.use_xflux}")
            # self.settings.use_redshift = True
            # self.settings.use_xflux = False
        # else:
            # self.settings.use_redshift = False

        if self.settings.autostart:
            self.autostart.set_active(True)
        else:
            self.autostart.set_active(False)

    def preview_click_event(self, widget, data=None):
        colsetting_temperature = settings.key_to_temperature(
            self.colsetting.get_active())
        self.redshift_controller.preview_color(colsetting_temperature)

    def delete_event(self, widget, data=None):
        if self.settings.latitude != self.latsetting.get_text():
            self.redshift_controller.set_latitude(
                self.latsetting.get_text())

        if self.settings.longitude != self.lonsetting.get_text():
            self.redshift_controller.set_longitude(
                self.lonsetting.get_text())

        if self.settings.zipcode != self.zipsetting.get_text():
            self.redshift_controller.set_xflux_zipcode(
                self.zipsetting.get_text())

        colsetting_temperature = settings.key_to_temperature(
            self.colsetting.get_active())
        if self.settings.color != colsetting_temperature:
            self.redshift_controller.color = colsetting_temperature

        if self.autostart.get_active():
            self.redshift_controller.set_autostart(True)
        else:
            self.redshift_controller.set_autostart(False)
        # if self.latsetting.get_text() == "" \
                # and self.zipsetting.get_text() == "":
            # self.display_no_zipcode_or_latitude_error_box()
            # return True

        self.window.hide()
        return True
