import fluxgui.settings as settings
from fluxgui.controller import Controller
from fluxgui.exceptions import XfluxError


class RedshiftController(Controller):
    def __init__(self, color=settings.default_temperature, pause_color=settings.off_temperature,
                 **kwargs):
        if 'longitude' not in kwargs or 'latitude' not in kwargs:
            raise XfluxError(
                "Required key not found (either longitude or latitude)")

        self._latitude = kwargs["latitude"]
        self._longitude = kwargs["longitude"]
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

        if "latitude" in kwargs:
            self._latitude = kwargs["latitude"]

        if "longitude" in kwargs:
            self._longitude = kwargs["longitude"]

        startup_args += ["-l", f"{self._latitude}:{self._longitude}"]
        startup_args += ["-t", f"6500:{color}"]

        return startup_args

    def _change_color_immediately(self, new_color):
        self._set_screen_color(new_color)

    def _set_screen_color(self, color):
        self._reset_color()
        self._start(self._create_startup_arg_list(color, **self.init_kwargs))

    def _set_setting(self, **kwargs):
        self._reset_color()
        self._start(self._create_startup_arg_list(**kwargs))

    def _reset_color(self):
        # start redshift with option "-x" to reset
        # the color back to normal
        self._start(startup_args=["redshift", "-x"])

    def _stop(self):
        # if we use the super class _stop() redshift ends without changing the color
        # back to normal, so we need to reset the color
        self._reset_color()
        return True
