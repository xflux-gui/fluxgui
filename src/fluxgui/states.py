from fluxgui.exceptions import MethodUnavailableError
import weakref


class _State(object):
    can_change_settings = False

    def __init__(self, controller_instance):
        self.name = str(controller_instance).capitalize()
        self.controller_ref = weakref.ref(controller_instance)

    def start(self, startup_args):
        raise MethodUnavailableError(
                "{} cannot start in its current state".format(self.name))

    def stop(self):
        raise MethodUnavailableError(
                "{} cannot stop in its current state".format(self.name))

    def preview(self, preview_color):
        raise MethodUnavailableError(
                "{} cannot preview in its current state".format(self.name))

    def toggle_pause(self):
        raise MethodUnavailableError(
                "{} cannot pause/unpause in its current state".format(self.name))

    def set_setting(self, **kwargs):
        raise MethodUnavailableError(
                "{} cannot alter settings in its current state".format(self.name))


class _InitState(_State):
    def start(self, startup_args):
        self.controller_ref()._start(startup_args)
        self.controller_ref().state = self.controller_ref().states["RUNNING"]

    def stop(self):
        return True

    def set_setting(self, **kwargs):
        for key, value in kwargs.items():
            self.controller_ref().init_kwargs[key] = str(value)


class _TerminatedState(_State):
    def stop(self):
        return True


class _AliveState(_State):
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
