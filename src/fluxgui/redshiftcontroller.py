from fluxgui import settings
from fluxgui.controller import Controller
from fluxgui.exceptions import XfluxError
from fluxgui.states import _InitState, _RunningState, _PauseState, _TerminatedState


class RedshiftController(Controller):
    def __init__(self, color=settings.default_temperature, pause_color=settings.off_temperature,
                 **kwargs):
        if 'longitude' not in kwargs and 'latitude' not in kwargs:
            raise XfluxError(
                "Required key not found (either longitude or latitude)")

        super(RedshiftController, self).__init__(color, pause_color, **kwargs)

        self.states = {
            "INIT": _InitState(self),
            "RUNNING": _RunningState(self),
            "PAUSED": _PauseState(self),
            "TERMINATED": _TerminatedState(self),
        }
        self.state = self.states["INIT"]

    def __repr__(self):
        return 'redshift'

    def _set_redshift_color(self, col):
        self.state.set_setting(color=col)

    def _get_xflux_color(self):
        return self.current_color

    color = property(_get_xflux_color, _set_redshift_color)

    def _create_startup_arg_list(self, color='3400', **kwargs):
        startup_args = ['redshift']
        if "latitude" in kwargs and kwargs['latitude']:
            startup_args += ["-l", f"{kwargs['latitude']}:{kwargs['longitude']}"]
            if "color" in kwargs and kwargs["color"]:
                startup_args += ["-t", f"6500K:{color}"]

        return startup_args

    def _change_color_immediately(self, new_color):
        self._set_screen_color(new_color)

    def _set_screen_color(self, color):
        self.current_color = color
        self._start()


class RedshiftSettings(RedshiftController):
    """
    RedshiftSettings is the same as RedshiftController except that it
    requires a Settings instance and updates that instance when
    relevant controller calls are made."""
    def __init__(self, settings):
        self.settings = settings
        super(RedshiftSettings, self).__init__(
            **self.settings.redshift_settings_dict())

    def start(self):
        if self.settings.longitude == "" and self.settings.latitude == "":
            raise ValueError("Cannot start redshift, missing longitude or latitude")
        super(RedshiftSettings, self).start()

    # Controller methods that don't touch xflux
    def set_autostart(self, autos):
        self.settings.autostart = autos

    # xflux methods that should also update settings
    def set_xflux_latitude(self, lat):
        self.settings.latitude = lat
        super(RedshiftSettings, self).set_latitude(lat)

    def set_xflux_longitude(self, longit):
        self.settings.longitude = longit
        super(RedshiftSettings, self).set_longitude(longit)

    def _set_xflux_color(self, col):
        self.settings.color = col
        super(RedshiftSettings, self)._set_color(col)

    def _get_xflux_color(self):
        return super(RedshiftSettings, self)._get_color()

    color = property(_get_xflux_color, _set_xflux_color)
