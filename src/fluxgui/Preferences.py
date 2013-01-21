import gtk
import gtk.glade
import os

class Preferences:
    """
    Information and methods related to the preferences window.
    Executes FluxController methods and gets data from Settings.
    """

    temperatureKeys = {
                0:  '2700',
                1:  '3400',
                2:  '4200',
                3:  '5000',
                4:  '6500',
                "off": '6500',
    }

    def temperature_to_key(self, temperature):
        for i, t in self.temperatureKeys.items():
            if t == temperature:
                return i

    def connect_widget(self, widget_name, connect_target=None,
            connect_event="activate"):
        widget = self.wTree.get_widget(widget_name)
        if connect_target:
            widget.connect(connect_event, connect_target)
        return widget


    def __init__(self, settings, xflux_controller):
        self.settings = settings
        self.xflux_controller = xflux_controller

        self.gladefile = os.path.join(os.path.dirname(os.path.dirname(
          os.path.realpath(__file__))), "fluxgui/preferences.glade")
        self.wTree = gtk.glade.XML(self.gladefile)

        self.window = self.connect_widget("window1", self.delete_event,
                connect_event="destroy")
        self.latsetting = self.connect_widget("entryLatitude",
                self.delete_event)
        self.lonsetting = self.connect_widget("entryLongitude",
                self.delete_event)
        self.zipsetting = self.connect_widget("entryZipcode",
                self.delete_event)
        self.colsetting = self.connect_widget("comboColor")
        self.colordisplay = self.connect_widget("labelCurrentColorTemperature")
        self.previewbutton = self.connect_widget("buttonPreview",
                self.preview_click_event, "clicked")
        self.closebutton = self.connect_widget("buttonClose",
                self.delete_event, "clicked")
        self.autostart = self.connect_widget("checkAutostart")

        if self.settings.latitude is "" and self.settings.zipcode is "":
            self.show()
            self.display_no_zipcode_or_latitude_error_box()


    def show(self):

        self.latsetting.set_text(self.settings.latitude)
        self.lonsetting.set_text(self.settings.longitude)
        self.zipsetting.set_text(self.settings.zipcode)
        self.colsetting.set_active(self.temperature_to_key(self.settings.color))
        self.colordisplay.set_text("Current color temperature: %sK"
                                    % (self.settings.color))
        if self.settings.autostart:
            self.autostart.set_active(True)
        else:
            self.autostart.set_active(False)

        self.window.show()

    def display_no_zipcode_or_latitude_error_box(self):
        md = gtk.MessageDialog(self.window,
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                gtk.BUTTONS_OK, "The f.lux indicator applet needs to know " +
                "your latitude or zipcode to work correctly. " +
                "Please fill either of them in on the preferences screen.")
        md.set_title("f.lux indicator applet")
        md.run()
        md.destroy()

    def preview_click_event(self, widget, data=None):
        colsetting_temperature = self.temperatureKeys[
                self.colsetting.get_active()]
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

        colsetting_temperature = self.temperatureKeys[
                self.colsetting.get_active()]
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

