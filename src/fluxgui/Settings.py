from GConfClient import GConfClient
import gtk # get out

class Settings(object):

    def __init__(self):
        self.client=GConfClient("/apps/fluxgui")

        # TODO: colortemp
        self._color=self.client.get_client_string("color",3400)
        self._autostart=self.client.get_client_string("autostart",0)
        self._latitude=self.client.get_client_string("latitude")
        self._longitude=self.client.get_client_string("longitude")
        self._zipcode=self.client.get_client_string("zipcode")

    def xflux_settings_dict(self):
        d={
                'color': self.color,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'zipcode': self.zipcode,
                'pause_color': self.off_color
        }
        return d

    # TODO: remove
    _temperatureKeys={
                0:  2700,
                1:  3400,
                2:  4200,
                3:  5000,
                4:  6500,
                "off": 6500,
            }
    off_color=_temperatureKeys["off"]

    def _get_color(self):
        return str(self._color)
    def _set_color(self,value):
        self._color=color
    #    self.client.set_client_string("color",value)
    #def _set_color_by_index(self,index):
    #    self._color=_temperatureKeys[value]


    # TODO: Try to get rid of colortemp

    #def _get_colortemp(self):
        #return self._colortemp
    #def _set_colortemp(self,value):
        #self._colortemp=_temperatureKeys[value]
    #    self.client.set_client_string("colortemp",value)


    def _get_latitude(self):
        return str(self._latitude)
    def _set_latitude(self,value):
        self._latitude=value
        self.client.set_client_string("latitude",value)

    def _get_longitude(self):
        return str(self._longitude)
    def _set_longitude(self,value):
        self._longitude=value
        self.client.set_client_string("longitude",value)

    def _get_zipcode(self):
        return str(self._zipcode)
    def _set_zipcode(self,value):
        self._zipcode=value
        self.client.set_client_string("zipcode",value)

    def _get_autostart(self):
        return self._autostart
    def _toggle_autostart(self,value):
        self._autostart=not self._autostart
        self.client.set_client_string("autostart", 1 if self._autostart else 0)

    color=property(_get_color, _set_color)
    #colortemp=property(self._get_colortemp, self._set_colortemp)
    latitude=property(_get_latitude,_set_latitude)
    longitude=property(_get_longitude,_set_longitude)
    zipcode=property(_get_zipcode,_set_zipcode)
    autostart=property(_get_autostart,_toggle_autostart)



