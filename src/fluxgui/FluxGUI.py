#!/usr/bin/python

import FluxController
import Settings
import Indicator
#import Preferences
import gtk
import sys, os
import signal
import errno

class FluxGUI(object):
    def __init__(self):
        self.check_pid()
        try:
            self.settings=Settings.Settings()
            self.xflux_controller=FluxController.FluxController(self.settings)
            self.indicator=Indicator.Indicator(self, self.xflux_controller)
        except Exception as e:
            print e
            print "Critical error. Exiting."
            sys.exit(1)

    def __del__(self):
        self.exit()

    def signal_exit(self, signum, frame):
        print 'Recieved signal: ', signum
        print 'Quitting...'
        self.exit()

    def exit(self):
        self.xflux_controller.stop()
        os.unlink(self.pidfile)
        gtk.main_quit()
        sys.exit()

    def run(self):
        gtk.main()

    def check_pid(self):
        pid = os.getpid()
        self.pidfile = os.path.expanduser("~/.fluxgui.pid")

        running = False # Innocent...
        if os.path.isfile(self.pidfile):
          try:
            oldpid = int(open(self.pidfile).readline().rstrip())
            try:
              os.kill(oldpid, 0)
              running = True # ...until proven guilty
            except OSError as err:
              if err.errno == errno.ESRCH:
                # OSError: [Errno 3] No such process
                print "stale pidfile, old pid: ", oldpid
          except ValueError:
            # Corrupt pidfile, empty or not an int on first line
            pass
        if running:
          print "fluxgui is already running, exiting"
          sys.exit()
        else:
          file(self.pidfile, 'w').write("%d\n" % pid)


if __name__ == '__main__':
    try:
        app=FluxGUI()
        signal.signal(signal.SIGTERM, app.signal_exit)
        app.run()
    except KeyboardInterrupt:
        app.exit()

