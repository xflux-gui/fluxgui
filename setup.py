#!/usr/bin/env python

from distutils.core import setup

setup(name = "f.lux indicator applet",
    version = "1.0.0",
    description = "f.lux indicator applet - better lightning...for your computer",
    author = "Kilian Valkhof",
    author_email = "kilian@kilianvalkhof.com",
    url = "http://fluxgui.kilianvalkhof.com",
    license = "MIT license",
      packages=['fluxgui'],
      package_dir={'fluxgui': 'src/fluxgui'},
      scripts=['fluxgui'],
      data_files=[
        ('bin', ['xflux']),
        ('share/icons/hicolor/scalable/apps', ['desktop/fluxgui.svg']),
        ('share/applications', ['desktop/fluxgui.desktop']),
		    ('share/pixmaps', ['fluxgui.svg', 'fluxgui-dark.svg', 'fluxgui-light.svg'])],
    long_description = """f.lux indicator applet is an indicator applet to
    control xflux, an application that makes the color of your computer's
    display adapt to the time of day, warm at nights and like sunlight during
    the day""",
  )

