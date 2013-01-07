import XfluxController
import Settings

class FluxController(XfluxController.XfluxController):
    def __init__(self):
        self.settings=Settings.Settings()
        super(FluxController, self).__init__(**self.settings.xflux_settings_dict())

    def __init__(self, settings):
        self.settings=settings
        super(FluxController, self).__init__(**self.settings.xflux_settings_dict())

    # xflux methods that update settings
    def set_xflux_latitude(self,latitude):
        self.settings.latitude=latitude
        super(FluxController, self).set_xflux_latitude(latitude)

    def set_xflux_longitude(self,longitude):
        self.settings.longitude=longitude
        super(FluxController, self).set_xflux_longitude(longitude)

    def set_xflux_zipcode(self,zipcode):
        self.settings.zipcode=zipcode
        super(FluxController, self).set_xflux_zipcode(zipcode)

    def _set_xflux_color(self,color):
        self.settings.color=color
        super(FluxController, self)._set_xflux_color(color)



