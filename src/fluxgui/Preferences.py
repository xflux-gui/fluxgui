import gtk
import gtk.glade
import os

class Preferences:

    temperatureKeys={
                0:  2700,
                1:  3400,
                2:  4200,
                3:  5000,
                4:  6500,
                "off": 6500,
    }

    def temperature_to_key(self, temperature):
        for i, t in self.temperatureKeys.items():
            if t==temperature:
                return i

    def __init__(self, settings, xflux_controller):
        self.settings=settings
        self.xflux_controller=xflux_controller

        self.gladefile = os.path.join(os.path.dirname(os.path.dirname(
          os.path.realpath(__file__))), "fluxgui/preferences.glade")
        self.wTree = gtk.glade.XML(self.gladefile)

        self.window = self.wTree.get_widget("window1")
        self.window.connect("destroy", self.delete_event)

        self.latsetting = self.wTree.get_widget("entryLatitude")
        self.latsetting.set_text(self.settings.latitude)
        self.latsetting.connect("activate", self.delete_event)

        self.lonsetting = self.wTree.get_widget("entryLongitude")
        self.lonsetting.set_text(self.settings.longitude)
        self.lonsetting.connect("activate", self.delete_event)

        self.zipsetting = self.wTree.get_widget("entryZipcode")
        self.zipsetting.set_text(self.settings.zipcode)
        self.zipsetting.connect("activate", self.delete_event)

        self.colsetting = self.wTree.get_widget("comboColor")
        colsetting_index=self.temperature_to_key(int(self.settings.color))
        self.colsetting.set_active(colsetting_index)
        # TODO? connect colsetting

        self.colordisplay = self.wTree.get_widget("labelCurrentColorTemperature")
        self.colordisplay.set_text("Current color temperature: "
                                       + str(self.settings.color) + "K")

        self.previewbutton = self.wTree.get_widget("buttonPreview")
        #TODO: wat
        self.previewbutton.connect("clicked", self.xflux_controller.preview_color)


        self.closebutton = self.wTree.get_widget("buttonClose")
        self.closebutton.connect("clicked", self.delete_event)

        self.autostart = self.wTree.get_widget("checkAutostart")
        if self.settings.autostart is "1":
            self.autostart.set_active(True)
        else:
            self.autostart.set_active(False)

        if self.settings.latitude is "" and self.settings.zipcode is "":
            self.display_no_zipcode_or_latitude_error()
            self.window.show()

    def show(self):
        self.window.show()

    def display_no_zipcode_or_latitude_error_box(self):
        md = gtk.MessageDialog(self.window,
                gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                gtk.BUTTONS_OK, "The f.lux indicator applet needs to know " +
                "your latitude or zipcode to work correctly. " +
                "Please fill either of them in on the preferences screen and then hit enter.")
        md.set_title("f.lux indicator applet")
        md.run()
        md.destroy()


    def delete_event(self, widget, data=None):
       
        if self.settings.latitude != self.latsetting.get_text():
            self.xflux_controller.set_xflux_latitude(self.latsetting.get_text())

        if self.settings.longitude != self.lonsetting.get_text():
            self.xflux_controller.set_xflux_longitude(self.lonsetting.get_text())

        if self.settings.zipcode != self.zipsetting.get_text():
            self.xflux_controller.set_xflux_zipcode(self.zipsetting.get_text())

        colsetting_temperature=\
                str(self.temperatureKeys[self.colsetting.get_active()])
        if str(self.settings.color) != colsetting_temperature:
            self.xflux_controller.color=colsetting_temperature

        #TODO: autostarter
        #if self.autostart.get_active():
            #self.main.create_autostarter()
        #else:
            #self.main.delete_autostarter()
        if self.latsetting.get_text()=="" and self.zipsetting.get_text()=="":
            self.display_no_zipcode_or_latitude_error_box()
            return True
 
        self.window.hide()
        return False

