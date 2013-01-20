import XfluxController
import Settings

class FluxController(XfluxController.XfluxController):
    def __init__(self):
        self.settings=Settings.Settings()
        super(FluxController, self).__init__(**self.settings.xflux_settings_dict())

    def __init__(self, settings):
        self.settings=settings
        #TODO: tmp
        self.settings.latitude=35
        self.settings.longitude=0
        super(FluxController, self).__init__(**self.settings.xflux_settings_dict())

    def start(self):
        if self.settings.zipcode=="" and self.settings.latitude=="":
            raise ValueError("Cannot start xflux, missing zipcode and latitude")
        super(FluxController, self).start()


    # xflux methods that should also update settings
    def set_xflux_latitude(self,lat):
        self.settings.latitude=lat
        super(FluxController, self).set_xflux_latitude(lat)

    def set_xflux_longitude(self,longit):
        self.settings.longitude=longit
        super(FluxController, self).set_xflux_longitude(longit)

    def set_xflux_zipcode(self,zipc):
        self.settings.zipcode=zipc
        super(FluxController, self).set_xflux_zipcode(zipc)

    def _set_xflux_color(self,col):
        self.settings.color=col
        super(FluxController, self)._set_xflux_color(col)



