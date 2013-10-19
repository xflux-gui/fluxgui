import pexpect
import time
import weakref
from fluxgui.exceptions import *

class XfluxController(object):
    """
    A controller that starts and interacts with an xflux process.
    """


    def __init__(self, color='3400', pause_color='6500', **kwargs):
        if 'zipcode' not in kwargs and 'latitude' not in kwargs:
            raise XfluxError(
                    "Required key not found (either zipcode or latitude)")
        if 'longitude' not in kwargs:
            kwargs['longitude'] = 0
        self.init_kwargs = kwargs
        self._current_color = str(color)
        self._pause_color = str(pause_color)

        self.states = {
            "INIT": _InitState(self),
            "RUNNING": _RunningState(self),
            "PAUSED": _PauseState(self),
            "TERMINATED": _TerminatedState(self),
        }
        self.state = self.states["INIT"]

    def start(self, startup_args=None):
        self.state.start(startup_args)

    def stop(self):
        self.state.stop()

    def preview_color(self, preview_color):
        self.state.preview(preview_color)

    def toggle_pause(self):
        self.state.toggle_pause()

    def set_xflux_latitude(self, lat):
        self.state.set_setting(latitude=lat)

    def set_xflux_longitude(self, longit):
        self.state.set_setting(longitude=longit)

    def set_xflux_zipcode(self, zipc):
        self.state.set_setting(zipcode=zipc)

    def _set_xflux_color(self, col):
        self.state.set_setting(color=col)

    def _get_xflux_color(self):
        self._c()
        index = self._xflux.expect("Color.*")
        color = -1
        if index == 0:
            color = self._xflux.after[10:14]
        return color

    color=property(_get_xflux_color, _set_xflux_color)

    def _start(self, startup_args=None):
        if not startup_args:
            startup_args = self._create_startup_arg_list(self._current_color,
                **self.init_kwargs)
        try:
            self._xflux = pexpect.spawn("xflux", startup_args)
                    #logfile=file("tmp/xfluxout.txt",'w'))

        except pexpect.ExceptionPexpect:
            raise FileNotFoundError(
                    "\nError: Please install xflux in the PATH \n")

    def _stop(self):
        try:
            if self._xflux.terminate(force=True):
                return True
            else:
                return False
        except Exception:
            # xflux has crashed in the meantime?
            return True

    def _preview_color(self, preview_color, return_color):
        # could probably be implemented better

        preview_color = str(preview_color)
        self._set_xflux_screen_color(preview_color)
        self._c()
        #while self.color != preview_color:
            #time.sleep(.5)
        time.sleep(5)
        self._set_xflux_screen_color(return_color)
        self._c()

    _settings_map = {
            'latitude':'l=',
            'longitude':'g=',
            'zipcode':'z=',
            'color':'k=',
    }

    def _set_xflux_setting(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._settings_map:
                if key == 'color':
                    self._set_xflux_screen_color(value)
                    self._current_color = str(value)
                    # hackish - changing the current color unpauses xflux,
                    # must reflect that with state change
                    if self.state == self.states["PAUSED"]:
                        self.state = self.states["RUNNING"]
                else:
                    self._xflux.sendline(self._settings_map[key]+str(value))
                self._c()

    def _create_startup_arg_list(self, color='3400', **kwargs):
        startup_args = []
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
        self._set_xflux_screen_color(new_color)
        self._c()

    def _p(self):
        # seems to bring color up to "off" then transitions back down (at night)
        # takes color down to night color then back up to off (during day)
        # I assume this is supposed to be "preview" or something like it
        # but it doesn't work the way it should for a preview so it isn't used
        self._xflux.sendline("p")

    def _c(self):
        # prints Colortemp=#### in xflux process
        # Also: When called after a color change (sendline(k=#))
        #   makes changes immediate
        #   (see use in toggle_pause() and preview_color())
        self._xflux.sendline("c")

    def _set_xflux_screen_color(self, color):
        # use _set_xflux_color unless keeping
        # self._current_color the same is necessary
        self._xflux.sendline("k="+str(color))


class _XfluxState(object):
    can_change_settings = False

    def __init__(self, controller_instance):
        self.controller_ref = weakref.ref(controller_instance)
    def start(self, startup_args):
        raise MethodUnavailableError(
                "Xflux cannot start in its current state")
    def stop(self):
        raise MethodUnavailableError(
                "Xflux cannot stop in its current state")
    def preview(self, preview_color):
        raise MethodUnavailableError(
                "Xflux cannot preview in its current state")
    def toggle_pause(self):
        raise MethodUnavailableError(
                "Xflux cannot pause/unpause in its current state")
    def set_setting(self, **kwargs):
        raise MethodUnavailableError(
                "Xflux cannot alter settings in its current state")

class _InitState(_XfluxState):
    def start(self, startup_args):
        self.controller_ref()._start(startup_args)
        self.controller_ref().state = self.controller_ref().states["RUNNING"]
    def stop(self):
        return True
    def set_setting(self, **kwargs):
        for key, value in kwargs.items():
            self.controller_ref().init_kwargs[key] = str(value)

class _TerminatedState(_XfluxState):
    def stop(self):
        return True

class _AliveState(_XfluxState):
    can_change_settings = True
    def stop(self):
        success = self.controller_ref()._stop()
        if success:
            self.controller_ref().state = \
                self.controller_ref().states["TERMINATED"]
        return success
    def set_setting(self, **kwargs):
        self.controller_ref()._set_xflux_setting(**kwargs)

class _RunningState(_AliveState):
    def toggle_pause(self):
        self.controller_ref()._change_color_immediately(
                self.controller_ref()._pause_color)
        self.controller_ref().state = self.controller_ref().states["PAUSED"]
    def preview(self, preview_color):
        self.controller_ref()._preview_color(preview_color,
                self.controller_ref()._current_color)

class _PauseState(_AliveState):
    def toggle_pause(self):
        self.controller_ref()._change_color_immediately(
                self.controller_ref()._current_color)
        self.controller_ref().state = self.controller_ref().states["RUNNING"]
    def preview(self, preview_color):
        self.controller_ref()._preview_color(preview_color,
                self.controller_ref()._pause_color)
