f.lux indicator applet
======================
_Better lighting for your computer_

The f.lux indicator applet `fluxgui` is an indicator applet to control
`xflux`, an application that makes the color of your computer's
display adapt to the time of day: warm at night, and like sunlight
during the day. Reducing blue light exposure in the evening can help
you fall asleep at night. See https://justgetflux.com/research.html
for more details.

This project -- https://github.com/xflux-gui/fluxgui -- is only
concerned with the `fluxgui` indicator applet program, not with the
underlying `xflux` program the indicator applet controls. The `xflux`
program is responsible for actually changing the color of your
screen. See https://justgetflux.com/linux.html for more information
about `xflux`.

`xflux` is downloaded automatically when installing `fluxgui`. Simply
run `fluxgui` in your terminal after installation to open the applet.
You can also easily configure the applet to auto-start on login.

Install Instructions
--------------------

### Only Python 3 is Supported

The `fluxgui` is only known to work with Python 3.

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
./download-xflux.py

# Compile GLIB schemas (temporary workaround until setup.py is fixed)
glib-compile-schemas .

# EITHER install system wide
sudo ./setup.py install --record installed.txt
xargs sudo chmod -R a+rX < installed.txt

# EXCLUSIVE OR, install in your home directory. The binary installs
# into ~/.local/bin, so be sure to add that to your PATH if installing
# locally. In particular, autostarting fluxgui in Gnome will not work
# if the locally installed fluxgui is not on your PATH.
./setup.py install --user --record installed.txt
       
# Run flux (the GSETTINGS_SCHEMA_DIR is temporary until setup.py is updated)
GSETTINGS_SCHEMA_DIR=. fluxgui
```

### Manual Uninstall

If you manually installed instead of using package manager, you can uninstall
by making `setup.py` tell you where it installed files and then
removing the installed files.

```bash
# EITHER uninstall globally
sudo ./setup.py install --record installed.txt
sudo xargs rm -vr < installed.txt

# EXCLUSIVE OR uninstall in your home directory
./setup.py install --user --record installed.txt
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
./download-xflux.py
glib-compile-schemas .
GSETTINGS_SCHEMA_DIR=`pwd` PATH=`pwd`:$PATH PYTHONPATH=`pwd`/src:$PYTHONPATH ./fluxgui
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
