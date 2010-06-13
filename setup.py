#!/usr/bin/env python

from distutils.core import setup

setup(name = "fluxgui",
    version = "1.0.0",
    description = "fluxgui - a gnome-applet to control xflux",
    author = "Kilian Valkhof",
    author_email = "kilian@kilianvalkhof.com",
    url = "http://fluxgui.kilianvalkhof.com",
    license = "MIT license",
      packages=['fluxgui'],
      package_dir={'fluxgui': 'src/fluxgui'},
      package_data={'fluxgui': ['pixmaps/*.*']},
      scripts=['fluxgui'],
      data_files=[
        ('share/icons/hicolor/scalable/apps', ['desktop/fluxgui.svg']),
        ('share/applications', ['desktop/fluxgui.desktop']),
		    ('share/pixmaps', ['fluxgui.svg', 'fluxgui-dark.svg', 'fluxgui-light.svg'])],
    long_description = """longdesc""",
  )

