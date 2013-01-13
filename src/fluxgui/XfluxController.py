import pexpect
import sys
import time

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
        self.state='INIT' # TODO: replace state with better design
        self.startup_args=self._create_startup_arg_list(color,**kwargs)

    def __del__(self):
        if self.state not in ["INIT","TERMINATED"]:
            self.stop()

    def set_xflux_latitude(self,latitude):
        self._xflux.sendline("l="+str(latitude))

    def set_xflux_longitude(self,longitude):
        self._xflux.sendline("g="+str(longitude))

    def set_xflux_zipcode(self,zipcode):
        self._xflux.sendline("z="+str(zipcode))

    def preview_color(self,preview_color):
        # could probably be implemented better

        preview_color=str(preview_color)
        self._set_xflux_screen_color(preview_color)
        self._c()
        while self.color != preview_color:
            time.sleep(.5)
        time.sleep(2)
        if self.state=="RUNNING":
            self._set_xflux_screen_color(self._current_color)
        elif self.state=="PAUSED":
            self._set_xflux_screen_color(self._pause_color)
        self._c()

    def toggle_pause(self):
        if self.state=='RUNNING':
            self.state='PAUSED'
            self._set_xflux_screen_color(self._pause_color)
            self._c()
        elif self.state=='PAUSED':
            self.state='RUNNING'
            self._set_xflux_screen_color(self._current_color)
            self._c()

    def _get_xflux_color(self):
        self._c()
        index = self._xflux.expect("Color.*")
        color=-1
        if index == 0:
            color = self._xflux.after[10:14]
        return color

    def _set_xflux_color(self,color):
        self._set_xflux_screen_color(color)
        self._current_color=str(color)
        if self.state=="PAUSED":
            self.state=="RUNNING"

    color=property(_get_xflux_color,_set_xflux_color)

    def start(self,startup_args=None):
        if self.state=="RUNNING":
            raise Exception("xflux is already running.")
        if not startup_args:
            startup_args=self.startup_args
        self.state='RUNNING'
        try:
            self._xflux = pexpect.spawn("/usr/bin/xflux", startup_args,\
                    logfile=file("tmp/xfluxout.txt",'w'))

            # TODO: remove xflux logging
            self._xflux.logfile_read=file("tmp/xfluxout_read.txt","w")
            self._xflux.logfile_send=file("tmp/xfluxout_send.txt","w")

        except pexpect.ExceptionPexpect:
            raise Exception("\nError: Please install xflux in /usr/bin/ \n")

    def stop(self):
        try:
            if self._xflux.terminate(force=True):
                self.state="TERMINATED"
                return True
            else:
                return False
        except Exception, e:
            # xflux has crashed in the meantime?
            return True


    def _create_startup_arg_list(self, color='3400', **kwargs):
        startup_args=[]
        if "zipcode" in kwargs:
            startup_args+=["-z",str(kwargs["zipcode"])]
        if "latitude" in kwargs:
            # by default xflux seems to use latitude even if zipcode is given
            startup_args+=["-l",str(kwargs["latitude"])]
            if "longitude" in kwargs:
                startup_args+=["-g",str(kwargs["longitude"])]
        startup_args+=["-k",str(color),"-nofork"] # nofork is vital

        return startup_args

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


