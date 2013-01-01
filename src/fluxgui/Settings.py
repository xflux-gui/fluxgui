from GConfClient import GConfClient

class Settings:
    _temperatureKeys={
                0:  2700,
                1:  3400,
                2:  4200,
                3:  5000,
                4:  6500,
            }

    def _get_color(self):
        return self._color
    def _set_color(self,value):
        self._color=temperatureKeys[value]

        command = "k=" + self._color
        self.main.update_xflux(command)

    def _get_colortemp(self):
        return self._colortemp
    def _set_colortemp(self,value):
        self._colortemp=temperatureKeys[value]
        self.client.set_client_string("colortemp",value)


    def _get_latitude(self):
        return self._latitude
    def _set_latitude(self,value):
        self._latitude=value

        # these should probably be moved
        self.client.set_client_string("latitude",value)
        command = "l=" + value
        self.main.update_xflux(command)

    def _get_longitude(self):
        return self._longitude
    def _set_longitude(self,value):
        self._longitude=value

        self.client.set_client_string("longitude",value)
        command = "g=" + value
        self.main.update_xflux(command)

    def _get_zipcode(self):
        return self._zipcode
    def _set_zipcode(self,value):
        self._zipcode=value

        self.client.set_client_string("zipcode",value)
        command = "z=" + value
        self.main.update_xflux(command)

    def _get_autostart(self):
        return self._autostart
    def _toggle_autostart(self,value):
        self._autostart=not self._autostart
        self.client.set_client_string("autostart",1 if self._autostart else 0)



    def __init__(self, main):
        self.main = main
        self.client=GConfClient()

        self._colortemp=self.client.get_client_string("colortemp",1)
        self._autostart=self.client.get_client_string("autostart",0)
        self._latitude=self.client.get_client_string("latitude")
        self._longitude=self.client.get_client_string("longitude")
        self._zipcode=self.client.get_client_string("zipcode")
        self._color=self.temperatureKeys[self.colortemp]

    color=property(self._get_color, self._set_color)
    colortemp=property(self._get_colortemp, self._set_colortemp)
    latitude=property(self._get_latitude,self._set_latitude)
    longitude=property(self._get_longitude,self._set_longitude)
    zipcode=property(self._get_zipcode,self._set_zipcode)
    autostart=property(self._get_autostart,self._toggle_autostart)

    def main(self):
        gtk.main()


