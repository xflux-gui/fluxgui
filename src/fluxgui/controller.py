import time
import pexpect
from fluxgui import settings


class Controller:
    def __init__(self, color=settings.default_temperature,
                 pause_color=settings.off_temperature, **kwargs):
        self.init_kwargs = kwargs
        self._current_color = color
        self._pause_color = pause_color

        self.states = {}
        self.state = None

    def start(self, startup_args=None):
        self.state.start(startup_args)

    def stop(self):
        self.state.stop()

    def preview_color(self, preview_color):
        self.state.preview(preview_color)

    def toggle_pause(self):
        self.state.toggle_pause()

    def set_latitude(self, lat):
        self.state.set_setting(latitude=lat)

    def set_longitude(self, longit):
        self.state.set_setting(longitude=longit)

    def _set_color(self, col):
        self.state.set_setting(color=col)

    def _kill(self, name):
        user_name = pexpect.run('whoami').decode('utf-8').strip()
        command = 'pgrep -d, -u {} {}'.format(user_name, name)
        previous_instances = pexpect.run(command).strip().decode('utf-8')

        if previous_instances != "":
            for process in previous_instances.split(","):
                pexpect.run('kill -9 {}'.format(process))

    def _start(self, startup_args=None):
        if not startup_args:
            startup_args = self._create_startup_arg_list(self._current_color,
                **self.init_kwargs)

        program = startup_args[0]

        try:
            self._kill(program)
            self.program = pexpect.spawn(program, startup_args[1:])
            # logfile=file("tmp/xfluxout.txt",'w'))

        except pexpect.ExceptionPexpect:
            raise FileNotFoundError("\nError: Please install {} in the PATH \n".format(program))

    def _preview_color(self, preview_color, return_color):
        # WIthout first setting the color to the off color, the
        # preview does nothing when the preview_color and return_color
        # are equal, which happens in daytime when you try to preview
        # your currently chosen nighttime color. Don't know if this is
        # a fluxgui bug or an xflux bug.
        self._change_color_immediately(settings.off_temperature)
        self._change_color_immediately(preview_color)
        time.sleep(5)
        self._change_color_immediately(return_color)

    def _stop(self):
        try:
            self._change_color_immediately(settings.off_temperature)
            # If we terminate xflux below too soon then the color
            # change doesn't take effect. Perhaps there's a more
            # gentle way to terminate xflux below -- the 'force=True'
            # means 'kill -9' ...
            time.sleep(1)
        except Exception as e:
            print('XfluxController._stop: unexpected exception when resetting color:')
            print(e)
        try:
            return self.program.terminate(force=True)
        except Exception as e:
            # xflux has crashed in the meantime?
            print('XfluxController._stop: unexpected exception when terminating xflux:')
            print(e)
            return True

    def _set_setting(self, **kwargs):
        """Should be implemented by child class."""
        raise NotImplementedError()

    def _change_color_immediately(self, new_color):
        """Should be implemented by child class."""
        raise NotImplementedError()

    def _set_screen_color(self, color):
        """Should be implemented by child class."""
        raise NotImplementedError()

    def _create_startup_arg_list(self, color='3400', **kwargs):
        """Should be implemented by child class."""
        raise NotImplementedError()
