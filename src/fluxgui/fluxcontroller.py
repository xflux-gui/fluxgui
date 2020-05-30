from fluxgui import xfluxcontroller

class FluxController(xfluxcontroller.XfluxController):
    """
    FluxController is the same as XfluxController except that it
    requires a Settings instance and updates that instance when
    relevant controller calls are made.
    """
    def __init__(self, settings):
        self.settings = settings
        super(FluxController, self).__init__(
                **self.settings.xflux_settings_dict())

    def __repr__(self):
        return 'Xflux'

    def start(self):
        if self.settings.zipcode == "" and self.settings.latitude == "":
            raise ValueError("Cannot start xflux, missing zipcode and latitude")
        super(FluxController, self).start()

    # Controller methods that don't touch xflux
    def set_autostart(self, autos):
        self.settings.autostart = autos

    # xflux methods that should also update settings
    def set_xflux_latitude(self, lat):
        self.settings.latitude = lat
        super(FluxController, self).set_latitude(lat)

    def set_xflux_longitude(self, longit):
        self.settings.longitude = longit
        super(FluxController, self).set_longitude(longit)

    def set_xflux_zipcode(self, zipc):
        self.settings.zipcode = zipc
        super(FluxController, self).set_xflux_zipcode(zipc)

    def _set_xflux_color(self, col):
        self.settings.color = col
        super(FluxController, self)._set_color(col)

    def _get_xflux_color(self):
        return super(FluxController, self)._get_color()

    color=property(_get_xflux_color, _set_xflux_color)
