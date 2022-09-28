from fluxgui.controller.redshift import RedshiftController


class RedshiftSettings(RedshiftController):
    """
    RedshiftSettings is the same as RedshiftController except that it
    requires a Settings instance and updates that instance when
    relevant controller calls are made."""
    def __init__(self, settings):
        self.new_settings = {}
        self.settings = settings
        super().__init__(**self.settings.redshift_settings_dict())

    def __repr__(self):
        return 'Redshift'

    def start(self):
        if self.new_settings:
            self._set_setting(**self.new_settings)
        else:
            super().start()

    # Controller methods that don't touch redshift
    def set_autostart(self, autos):
        self.settings.autostart = autos

    # redshift methods that should also update settings
    def set_redshift_latitude(self, lat):
        self.new_settings["latitude"] = lat
        self.settings.latitude = lat

    def set_redshift_longitude(self, longit):
        self.new_settings["longitude"] = longit
        self.settings.longitude = longit

    def _set_redshift_color(self, col):
        self.new_settings["color"] = col
        self.settings.color = col

    def _get_redshift_color(self):
        return self.settings.color

    color = property(_get_redshift_color, _set_redshift_color)
