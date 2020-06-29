from fluxgui import settings
from fluxgui.controller import Controller
from fluxgui.exceptions import XfluxError


class RedshiftController(Controller):
    def __init__(self, color=settings.default_temperature, pause_color=settings.off_temperature,
                 **kwargs):
        if 'longitude' not in kwargs and 'latitude' not in kwargs:
            raise XfluxError(
                "Required key not found (either longitude or latitude)")

        super().__init__(color, pause_color, **kwargs)

    def __repr__(self):
        return 'redshift'

    def _set_redshift_color(self, col):
        self.state.set_setting(color=col)

    def _get_redshift_color(self):
        return self._current_color

    color = property(_get_redshift_color, _set_redshift_color)

    def _create_startup_arg_list(self, color='3400', **kwargs):
        print(f"create_startup color={color} kwargs={kwargs}")
        startup_args = ['redshift']
        if "latitude" in kwargs and kwargs['latitude']:
            startup_args += ["-l", f"{kwargs['latitude']}:{kwargs['longitude']}"]
        startup_args += ["-t", f"6500:{color}"]

        return startup_args

    def _change_color_immediately(self, new_color):
        self._set_screen_color(new_color)

    def _set_screen_color(self, color):
        self._current_color = color
        self._start()

    def _set_setting(self, **kwargs):
        args = self._create_startup_arg_list(**kwargs)
        self._start(startup_args=args)


class RedshiftSettings(RedshiftController):
    """
    RedshiftSettings is the same as RedshiftController except that it
    requires a Settings instance and updates that instance when
    relevant controller calls are made."""
    def __init__(self, settings):
        self.settings = settings
        super(RedshiftSettings, self).__init__(
            **self.settings.redshift_settings_dict())

    def __repr__(self):
        return 'Redshift'

    def start(self):
        if self.settings.longitude == "" and self.settings.latitude == "":
            raise ValueError("Cannot start redshift, missing longitude or latitude")
        super(RedshiftSettings, self).start()

    # Controller methods that don't touch xflux
    def set_autostart(self, autos):
        self.settings.autostart = autos

    # xflux methods that should also update settings
    def set_redshift_latitude(self, lat):
        self.settings.latitude = lat
        super(RedshiftSettings, self).set_latitude(lat)

    def set_redshift_longitude(self, longit):
        self.settings.longitude = longit
        super(RedshiftSettings, self).set_longitude(longit)

    def _set_redshift_color(self, col):
        self.settings.color = col
        super(RedshiftSettings, self)._set_color(col)

    def _get_redshift_color(self):
        return super(RedshiftSettings, self)._get_color()

    color = property(_get_redshift_color, _set_redshift_color)