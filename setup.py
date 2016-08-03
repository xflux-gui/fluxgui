#!/usr/bin/env python

from distutils.core import setup
import os

data_files = [('share/icons/hicolor/scalable/apps', ['fluxgui.svg', 'fluxgui-light.svg', 'fluxgui-dark.svg']),
('share/applications', ['desktop/fluxgui.desktop'])]

if (os.path.exists("xflux")):
    data_files.append( ('bin', ['xflux']) )
else:
    print("""WARNING: if you are running 'python setup.py' manually, and not as
part of Debian package creation, then you need to install the 'xflux'
binary separately. You can do this by running

    python ./download-xflux.py

before running 'setup.py'.""")

setup(name = "f.lux indicator applet",
    version = "1.1.8",
    description = "f.lux indicator applet - better lighting for your computer",
    author = "Kilian Valkhof, Michael and Lorna Herf, Josh Winters",
    author_email = "kilian@kilianvalkhof.com",
    url = "http://www.stereopsis.com/flux/",
    license = "MIT license",
    package_dir = {'fluxgui' : 'src/fluxgui'},
    packages = ["fluxgui",],
    package_data = {"fluxgui" : ["*.glade"] },
    data_files=data_files,
    scripts = ["fluxgui"],
    long_description = """f.lux indicator applet is an indicator applet to
    control xflux, an application that makes the color of your computer's
    display adapt to the time of day, warm at nights and like sunlight during
    the day""",
  )

