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
        self._current_color = col
        self.state.set_setting(color=col)

    def _get_redshift_color(self):
        return self._current_color

    color = property(_get_redshift_color, _set_redshift_color)

    def _create_startup_arg_list(self, color='3400', **kwargs):
        startup_args = ['redshift']

        if "latitude" in kwargs and kwargs['latitude']:
            startup_args += ["-l", f"{kwargs['latitude']}:{kwargs['longitude']}"]
        startup_args += ["-t", f"6500:{color}"]

        return startup_args

    def _change_color_immediately(self, new_color):
        self._set_screen_color(new_color)

    def _set_screen_color(self, color):
        self._stop()
        self._start(startup_args=["redshift", "-O", color])

    def _set_setting(self, **kwargs):
        if "color" in kwargs and kwargs["color"]:
            self._stop()
        self._start(self._create_startup_arg_list(**kwargs))

    def _stop(self):
        # if we use the super class _stop() redshift ends without changing the color
        # back to normal, so we need to start redshift with option "-x" to reset 
        # the color back to normal.
        self._start(startup_args=["redshift", "-x"])
        return True


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
