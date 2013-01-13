import pexpect
import sys
import time
import weakref

class XfluxController(object):

    def __init__(self, color='3400', pause_color='6500', **kwargs):
        if 'zipcode' not in kwargs and 'latitude' not in kwargs:
            # one of these should be passed in, error otherwise
            raise Exception("Required key not found (either zipcode or latitude)")
        if 'longitude' not in kwargs:
            kwargs['longitude']=0
        self.init_kwargs=kwargs
        #
        self._current_color=str(color)
        self._pause_color=str(pause_color)
        self.startup_args=self._create_startup_arg_list(color,**kwargs)

        self.states={
            "INIT": InitState(self),
            "RUNNING": RunningState(self),
            "PAUSED": PauseState(self),
            "TERMINATED": TerminatedState(self),
        }
        self.state=self.states["INIT"]

    def start(self, startup_args=None):
        self.state.start(startup_args)

    def stop(self):
        self.state.stop()

    def preview_color(self, preview_color):
        self.state.preview(preview_color)

    def toggle_pause(self):
        self.state.toggle_pause()

    def set_xflux_latitude(self,latitude):
        if self.state.can_change_settings:
            self._xflux.sendline("l="+str(latitude))
        else:
            raise Exception("Cannot currently update xflux")

    def set_xflux_longitude(self,longitude):
        if self.state.can_change_settings:
            self._xflux.sendline("g="+str(longitude))
        else:
            raise Exception("Cannot currently update xflux")

    def set_xflux_zipcode(self,zipcode):
        if self.state.can_change_settings:
            self._xflux.sendline("z="+str(zipcode))
        else:
            raise Exception("Cannot currently update xflux")

    def _get_xflux_color(self):
        self._c()
        index = self._xflux.expect("Color.*")
        color=-1
        if index == 0:
            color = self._xflux.after[10:14]
        return color

    def _set_xflux_color(self,color):
        if self.state.can_change_settings:
            self._set_xflux_screen_color(color)
            self._current_color=str(color)

            # hackish
            if self.state==self.states["PAUSED"]:
                self.state==self.states["RUNNING"]
        else:
            raise Exception("Cannot currently update xflux")

    color=property(_get_xflux_color,_set_xflux_color)


    def _start(self,startup_args=None):
        if not startup_args:
            startup_args=self.startup_args
        try:
            self._xflux = pexpect.spawn("/usr/bin/xflux", startup_args,\
                    logfile=file("tmp/xfluxout.txt",'w'))

            # TODO: remove xflux logging
            self._xflux.logfile_read=file("tmp/xfluxout_read.txt","w")
            self._xflux.logfile_send=file("tmp/xfluxout_send.txt","w")

        except pexpect.ExceptionPexpect:
            raise Exception("\nError: Please install xflux in /usr/bin/ \n")


    def _stop(self):
        try:
            if self._xflux.terminate(force=True):
                return True
            else:
                return False
        except Exception, e:
            # xflux has crashed in the meantime?
            return True

    def _preview_color(self,preview_color, return_color):
        # could probably be implemented better

        preview_color=str(preview_color)
        self._set_xflux_screen_color(preview_color)
        self._c()
        while self.color != preview_color:
            time.sleep(.5)
        time.sleep(2)
        self._set_xflux_screen_color(return_color)

        #if self.state=="RUNNING":
            #self._set_xflux_screen_color(self._current_color)
        #elif self.state=="PAUSED":
            #self._set_xflux_screen_color(self._pause_color)
        #self._c()

    def _create_startup_arg_list(self, color='3400', **kwargs):
        startup_args=[]
        if "zipcode" in kwargs:
            startup_args+=["-z",str(kwargs["zipcode"])]
        if "latitude" in kwargs:
            # by default xflux uses latitude even if zipcode is given
            startup_args+=["-l",str(kwargs["latitude"])]
            if "longitude" in kwargs:
                startup_args+=["-g",str(kwargs["longitude"])]
        startup_args+=["-k",str(color),"-nofork"] # nofork is vital

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
        # prints Colortemp=####
        # Also: When called after a color change (sendline(k=#)) makes changes immediate
        #   (see use in toggle_pause() and preview_color())
        self._xflux.sendline("c")

    def _set_xflux_screen_color(self,color):
        # use _set_xflux_color unless keeping self._current_color the same is necessary
        self._xflux.sendline("k="+str(color))


class XfluxState(object):
    can_change_settings=False

    def __init__(self, controller_instance):
        self.controller_ref=weakref.ref(controller_instance)
    def start(self, startup_args):
        pass
    def stop(self):
        pass
    def preview(self, preview_color):
        pass
    def toggle_pause(self):
        pass

class InitState(XfluxState):
    def start(self, startup_args):
        self.controller_ref()._start(startup_args)
        self.controller_ref().state=self.controller_ref().states["RUNNING"]
    def stop(self):
        return True

class TerminatedState(XfluxState):
    def start(self, startup_args):
        pass
    def stop(self):
        return True

class AliveState(XfluxState):
    can_change_settings=True
    def start(self, startup_args):
        raise Exception("xflux is already running.")
    def stop(self):
        success=self.controller_ref()._stop()
        if success:
            self.controller_ref().state=self.controller_ref().states["TERMINATED"]
        return success

class RunningState(AliveState):
    def toggle_pause(self):
        self.controller_ref()._change_color_immediately(\
                self.controller_ref()._pause_color)
        self.controller_ref().state=self.controller_ref().states["PAUSED"]
    def preview(self, preview_color):
        self.controller_ref()._preview_color(preview_color,\
                self.controller_ref()._current_color)

class PauseState(AliveState):
    def toggle_pause(self):
        self.controller_ref()._change_color_immediately(\
                self.controller_ref()._current_color)
        self.controller_ref().state=self.controller_ref().states["RUNNING"]
    def preview(self, preview_color):
        self.controller_ref()._preview_color(preview_color,\
                self.controller_ref()._pause_color)
