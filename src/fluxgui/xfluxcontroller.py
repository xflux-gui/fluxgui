from fluxgui import settings
from fluxgui.exceptions import XfluxError
from fluxgui.controller import Controller
from fluxgui.states import _InitState, _RunningState, _PauseState, _TerminatedState


class XfluxController(Controller):
    """
    A controller that starts and interacts with an xflux process.
    """

    def __init__(self, color=settings.default_temperature, pause_color=settings.off_temperature, **kwargs):
        if 'zipcode' not in kwargs and 'latitude' not in kwargs:
            raise XfluxError(
                    "Required key not found (either zipcode or latitude)")
        if 'longitude' not in kwargs:
            kwargs['longitude'] = 0

        super(XfluxController, self).__init__(color, pause_color, **kwargs)

        self.states = {
            "INIT": _InitState(self),
            "RUNNING": _RunningState(self),
            "PAUSED": _PauseState(self),
            "TERMINATED": _TerminatedState(self),
        }
        self.state = self.states["INIT"]

    def __repr__(self):
        return 'xflux'

    def set_xflux_zipcode(self, zipc):
        self.state.set_setting(zipcode=zipc)

    def _set_xflux_color(self, col):
        self.state.set_setting(color=col)

    def _get_xflux_color(self):
        self._c()
        index = self.program.expect("Color.*")
        color = -1
        if index == 0:
            color = self.program.after[10:14]
        return color

    color=property(_get_xflux_color, _set_xflux_color)

    _settings_map = {
            'latitude':'l=',
            'longitude':'g=',
            'zipcode':'z=',
            'color':'k=',
    }

    def _set_setting(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._settings_map:
                if key == 'color':
                    self._set_screen_color(value)
                    self._current_color = str(value)
                    # hackish - changing the current color unpauses xflux,
                    # must reflect that with state change
                    if self.state == self.states["PAUSED"]:
                        self.state = self.states["RUNNING"]
                else:
                    self.program.sendline(self._settings_map[key]+str(value))
                self._c()

    def _create_startup_arg_list(self, color='3400', **kwargs):
        startup_args = ['xflux']
        if "zipcode" in kwargs and kwargs['zipcode']:
            startup_args += ["-z", str(kwargs["zipcode"])]
        if "latitude" in kwargs and kwargs['latitude']:
            # by default xflux uses latitude even if zipcode is given
            startup_args += ["-l", str(kwargs["latitude"])]
        if "longitude" in kwargs and kwargs['longitude']:
            startup_args += ["-g", str(kwargs["longitude"])]
        startup_args += ["-k", str(color), "-nofork"] # nofork is vital

        return startup_args

    def _change_color_immediately(self, new_color):
        self._set_screen_color(new_color)
        self._c()

    def _p(self):
        # seems to bring color up to "off" then transitions back down (at night)
        # takes color down to night color then back up to off (during day)
        # I assume this is supposed to be "preview" or something like it
        # but it doesn't work the way it should for a preview so it isn't used
        self.program.sendline("p")

    def _c(self):
        # prints Colortemp=#### in xflux process
        # Also: When called after a color change (sendline(k=#))
        #   makes changes immediate
        #   (see use in toggle_pause() and preview_color())
        self.program.sendline("c")

    def _set_screen_color(self, color):
        # use _setprogram_color unless keeping
        # self._current_color the same is necessary
        self.program.sendline("k={}".format(str(color)))
