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

See [ubuntuhandbook.org instructions](http://ubuntuhandbook.org/index.php/2016/03/install-f-lux-in-ubuntu-16-04/) for more details on using the PPA to install xflux using the package manager. *Until the PPA is updated to `xflux-gui` version 1.1.9, it's probably better to install from source.*

### Ubuntu/Debian Manual Install

```bash
# Install dependencies
sudo apt-get install git python-appindicator python-xdg python-pexpect python-gconf python-gtk2 python-glade2 libxxf86vm1 -y

# Download and install xflux-gui
cd /tmp
git clone "https://github.com/xflux-gui/xflux-gui.git"
cd xflux-gui
sudo python ./setup.py install

# Run flux
fluxgui
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
