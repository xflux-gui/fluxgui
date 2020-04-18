from fluxgui.exceptions import MethodUnavailableError
import weakref


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
        self.controller_ref()._set_setting(**kwargs)


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
