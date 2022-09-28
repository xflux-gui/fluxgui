#!/usr/bin/env python3

from distutils.core import setup
from distutils.log import info
import distutils.command.install_data
import os, os.path, subprocess, sys

if os.path.abspath(os.path.curdir) != os.path.abspath(os.path.dirname(__file__)):
    print("The 'setup.py' must be run in its containing directory!")
    sys.exit(1)

# Set an appropriate umask for global installs. The 'setup.py' install
# respects the umask, even if it results in files only root can read
# in a global install :P
os.umask(0o022)

# Set appropriate permissions on all local files in the repo. The
# 'setup.py' install preserves permissions on copied files, which
# creates problems for global installs :P
#
# There is a fancier solution at
# https://stackoverflow.com/a/25761434/470844 that uses
# 'self.get_outputs()' in a custom 'distutils.command.install'
# subclass to only modify permissions of files that 'setup.py'
# installed.
subprocess.call(['chmod', '-R', 'a+rX', '.'])

# On Ubuntu 18.04 both '/usr/local/share/glib-2.0/schemas' (global
# install) and '~/.local/share/glib-2.0/schemas' (local '--user'
# install) are on the default search path for glib schemas. The global
# search paths are in '$XDG_DATA_DIRS'.
gschema_dir_suffix = 'share/glib-2.0/schemas'

data_files = [
    ('share/icons/hicolor/16x16/apps', ['icons/hicolor/16x16/apps/fluxgui.svg']),
    ('share/icons/hicolor/22x22/apps', ['icons/hicolor/22x22/apps/fluxgui.svg']),
    ('share/icons/hicolor/24x24/apps', ['icons/hicolor/24x24/apps/fluxgui.svg']),
    ('share/icons/hicolor/32x32/apps', ['icons/hicolor/32x32/apps/fluxgui.svg']),
    ('share/icons/hicolor/48x48/apps', ['icons/hicolor/48x48/apps/fluxgui.svg']),
    ('share/icons/hicolor/64x64/apps', ['icons/hicolor/64x64/apps/fluxgui.svg']),
    ('share/icons/hicolor/96x96/apps', ['icons/hicolor/96x96/apps/fluxgui.svg']),
    ('share/icons/ubuntu-mono-dark/status/16', ['icons/ubuntu-mono-dark/status/16/fluxgui-panel.svg']),
    ('share/icons/ubuntu-mono-dark/status/22', ['icons/ubuntu-mono-dark/status/22/fluxgui-panel.svg']),
    ('share/icons/ubuntu-mono-dark/status/24', ['icons/ubuntu-mono-dark/status/24/fluxgui-panel.svg']),
    ('share/icons/ubuntu-mono-light/status/16', ['icons/ubuntu-mono-light/status/16/fluxgui-panel.svg']),
    ('share/icons/ubuntu-mono-light/status/22', ['icons/ubuntu-mono-light/status/22/fluxgui-panel.svg']),
    ('share/icons/ubuntu-mono-light/status/24', ['icons/ubuntu-mono-light/status/24/fluxgui-panel.svg']),
    ('share/icons/Adwaita/16x16/status', ['icons/Adwaita/16x16/status/fluxgui-panel.svg']),
    ('share/icons/breeze/status/22', ['icons/breeze/status/22/fluxgui-panel.svg']),
    ('share/icons/breeze-dark/status/22', ['icons/breeze-dark/status/22/fluxgui-panel.svg']),
    ('share/icons/elementary/status/24', ['icons/elementary/status/24/fluxgui-panel.svg']),
    ('share/icons/elementary-xfce/panel/22', ['icons/elementary-xfce/panel/22/fluxgui-panel.svg']),
    ('share/icons/elementary-xfce-dark/panel/22', ['icons/elementary-xfce-dark/panel/22/fluxgui-panel.svg']),
    ('share/applications', ['desktop/fluxgui.desktop']),
    (gschema_dir_suffix, ['apps.fluxgui.gschema.xml'])]

scripts = ['fluxgui']

if (os.path.exists("xflux")):
    # Unlike for 'scripts', the 'setup.py' doesn't modify the
    # permissions on files installed using 'data_files', so we need to
    # set the permissions ourselves.
    subprocess.call(['chmod', 'a+rx', 'xflux'])
    data_files.append(('bin', ['xflux']))
else:
    print("""WARNING: if you are running 'python setup.py' manually, and not as
part of Debian package creation, then you need to download the 'xflux'
binary separately. You can do this by running

    ./download-xflux.py

before running 'setup.py'.""")

class install_data(distutils.command.install_data.install_data):
    def run(self):
        super().run()

        # Compile '*.gschema.xml' to update or create 'gschemas.compiled'.
        if os.environ.get('DISABLE_GSCHEMAS_COMPILED') is None:
            info("compiling gsettings schemas; set DISABLE_GSCHEMAS_COMPILED env var to disable")
            gschema_dir = os.path.join(self.install_dir, gschema_dir_suffix)
            self.spawn(["glib-compile-schemas", gschema_dir])

setup(name = "f.lux indicator applet",
    version = "2.0",
    description = "f.lux indicator applet - better lighting for your computer",
    author = "Kilian Valkhof, Michael and Lorna Herf, Josh Winters",
    author_email = "kilian@kilianvalkhof.com",
    url = "http://www.stereopsis.com/flux/",
    license = "MIT license",
    package_dir = {'fluxgui' : 'src/fluxgui'},
    packages = ["fluxgui", "fluxgui.settings", "fluxgui.controller", "fluxgui.tabs"],
    package_data = {"fluxgui" : ["*.glade"] },
    data_files=data_files,
    scripts = scripts,
    long_description = """f.lux indicator applet is an indicator applet to
    control xflux, an application that makes the color of your computer's
    display adapt to the time of day, warm at nights and like sunlight during
    the day""",
    cmdclass = {'install_data': install_data}
  )
