f.lux indicator applet
======================
Better lighting for your computer

The f.lux indicator applet `fluxgui` is an indicator applet to control
`xflux`, an application that makes the color of your computer's
display adapt to the time of day, warm at nights and like sunlight
during the day. Reducing blue light exposure in the evening can help
you fall asleep at night. See https://justgetflux.com/research.html
for more details.

This project -- https://github.com/xflux-gui/fluxgui -- is only
concerned with the `fluxgui` indicator applet program, not with the
underlying `xflux` program the indicator applet controls. The `xflux`
program is responsible for actually changing the color of your
screen. See https://justgetflux.com/linux.html for more information
about `xflux`.

Install Instructions
--------------------

### Only Python 2 is Supported

The `fluxgui` is only known to work with Python 2, so use `python2` instead of `python` for the commands in this README if Python 3 is the default on your system.

### Ubuntu PPA Package Manager Install

To install via apt:

```bash
sudo add-apt-repository ppa:nathan-renniewaldock/flux
sudo apt-get update
sudo apt-get install fluxgui
```

See [ubuntuhandbook.org instructions](http://ubuntuhandbook.org/index.php/2016/03/install-f-lux-in-ubuntu-16-04/) for more details.

If you have trouble with the PPA version try the manual install below.

### Fedora Package Manager Install

There is no Fedora package provided yet. Please use [Manual Install](#manual-install) below.

### Manual Install

To install manually you first install the dependencies using your package manager, and then install `fluxgui` using the provided `setup.py`. The manual install can be done locally or system wide.

#### Install Dependencies Using Package Manager

##### Ubuntu/Debian

```bash
sudo apt-get install git python-appindicator python-xdg python-pexpect python-gconf python-gtk2 python-glade2 libxxf86vm1
```
##### Fedora/CentOS

```bash
sudo yum install git python-appindicator python2-pyxdg python2-pexpect gnome-python2-gconf pygtk2 pygtk2-libglade
```

#### Install `fluxgui`

There are separate instructions in the code below for installing system wide and for installing locally in your user directory; choose one.

```bash
# Download fluxgui
cd /tmp
git clone "https://github.com/xflux-gui/fluxgui.git"
cd fluxgui
python download-xflux.py

# EITHER install system wide
sudo python setup.py install

# EXCLUSIVE OR, install in your home directory. The binary installs
# into ~/.local/bin, so be sure to add that to your PATH if installing
# locally. In particular, autostarting fluxgui in Gnome will not work
# if the locally installed fluxgui is not on your PATH.
python setup.py install --user
       
# Run flux
fluxgui
```

### Manual Uninstall

If you manually installed instead of using package manager, you can uninstall
by making `setup.py` tell you where it installed files and then
removing the installed files.

```bash
# EITHER uninstall globally
sudo python setup.py install --record installed.txt
sudo xargs rm -vr < installed.txt

# EXCLUSIVE OR uinstall in your home directory
python setup.py install --user --record installed.txt
xargs rm -vr < installed.txt
```

License
-------

The f.lux indicator applet is released under the [MIT License](https://github.com/xflux-gui/fluxgui/blob/master/LICENSE).

Developing
----------

### Running `fluxgui` Without Installing

When working on `fluxgui`, you can use
```bash
cd <path to your fluxgui.git clone>
# You only need to download xflux once.
python download-xflux.py
PATH=`pwd`:$PATH PYTHONPATH=`pwd`/src:$PYTHONPATH ./fluxgui &
```
to test your local copy of `fluxgui` without installing anything.

### Change Logs, Versions, Releases

Note changes in `./debian/changelog`.

Use version `<ver>~pre` until ready to release a version. When
releasing a version make branch, remove the `~pre` suffix from the
version strings in the branch, and `git tag -a` the branch `v<ver>`.

When releasing the version string needs to be changed in
`debian/changelog` and `setup.py`, and the release dates needs to be
added in `debian/changelog`.
