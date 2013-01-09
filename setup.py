#!/usr/bin/env python

from distutils.core import setup

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
    data_files=[('share/icons/hicolor/scalable/apps', ['fluxgui.svg', 'fluxgui-light.svg', 'fluxgui-dark.svg']),
            ('share/applications', ['desktop/fluxgui.desktop']),
            ('bin', ['xflux']),],
    scripts = ["fluxgui"],
    long_description = """f.lux indicator applet is an indicator applet to
    control xflux, an application that makes the color of your computer's
    display adapt to the time of day, warm at nights and like sunlight during
    the day""",
  )

