f.lux indicator applet
======================
Better lighting for your computer

The f.lux indicator applet `fluxgui` is an indicator applet to control
`xflux`, an application that makes the color of your computer's
display adapt to the time of day, warm at nights and like sunlight
during the day. Reducing blue light exposure in the evening can help
you fall asleep at night. See https://justgetflux.com/research.html
for more details.

This project -- https://github.com/xflux-gui/xflux-gui -- is only
concerned with the `fluxgui` indicator applet program, not with the
underlying `xflux` program the indicator applet controls. The `xflux`
program is responsible for actually changing the color of your
screen. See https://justgetflux.com/linux.html for more information
about `xflux`.

Install Instructions
--------------------

### Ubuntu PPA Package Manager Install

There is a PPA here:

https://launchpad.net/~nathan-renniewaldock/+archive/ubuntu/flux

See [ubuntuhandbook.org instructions](http://ubuntuhandbook.org/index.php/2016/03/install-f-lux-in-ubuntu-16-04/) for more details on using the PPA to install xflux using the package manager.

If you have trouble with the PPA version try the manual install below.

### Ubuntu/Debian Manual Install

```bash
# Install dependencies
sudo apt-get install git python-appindicator python-xdg python-pexpect python-gconf python-gtk2 python-glade2 libxxf86vm1

# Download and install xflux-gui
cd /tmp
git clone "https://github.com/xflux-gui/xflux-gui.git"
cd xflux-gui
python download-xflux.py
sudo python setup.py install # OR: python setup.py install --local

# Run flux
fluxgui

# To uninstall:

sudo rm /usr/local/lib/python2.7/dist-packages/f.lux_indicator*
sudo rm -rf /usr/local/lib/python2.7/dist-packages/fluxgui
sudo rm -rf /usr/local/share/icons/hicolor/scalable/apps/fluxgui.*
sudo rm /usr/share/applications/fluxgui.desktop
sudo rm /usr/local/bin/xflux
sudo rm /usr/local/bin/fluxgui
```

License
-------

The f.lux indicator applet is released under the **MIT License**.

Developing
----------

When working on `fluxgui`, you can use
```bash
cd <path to your xflux-gui.git clone>
PYTHONPATH=`pwd`/src:$PYTHONPATH ./fluxgui &
```
to test your local copy of `fluxgui` without installing anything.
