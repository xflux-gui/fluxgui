import os
from gi.repository import Gio
from xdg.DesktopEntry import DesktopEntry
from fluxgui.exceptions import DirectoryCreationError

################################################################
# Color temperatures.

# The color options available in the color preferences dropdown in the
# "Preferences" GUI are defined in ./preferences.glade. Choosing a
# preference in the GUI returns a number, with 0 for the first choice,
# 1 for the second choice, etc.
default_temperature = '3400'
off_temperature = '6500'
temperatures = [
    '2000',  # The minimum supported by flux; see https://github.com/xflux-gui/xflux-gui/issues/51
    '2300',
    '2700',
    '3400',  # The 'default_temperature' needs to be one of the options!
    '4200',
    '5000',
    # The "off temperature" is not one of the menu choices, but
    # the previous code included it, so @ntc2 is leaving it in
    # without understanding why ...
    #
    # TODO(ntc2): understand why this entry is in the list, and remove
    # it if possible.
    off_temperature]


def key_to_temperature(key):
    """The inverse of 'temperature_to_key'.

    """
    # The old version of this code supported a special key "off". We
    # now map all unknown keys to "off", but I don't understand what
    # the "off" value is for.
    #
    # TODO(ntc2): figure out what the "off" value is for.
    try:
        return temperatures[key]
    except IndexError:
        return off_temperature


def temperature_to_key(temperature):
    """Convert a temperature like "3400" to a Glade/GTK menu value like
    "1" or "off".

    """
    for i, t in enumerate(temperatures):
        if t == temperature:
            return i
    # For invalid temperatures -- which should be impossible ? --
    # return the number corresponding to the off temperature. Perhaps
    # we could also return "off" here? But I have no idea how this
    # code is even triggered.
    return len(temperatures) - 1

################################################################


class Settings(object):

    def __init__(self):
        self.settings = Gio.Settings.new('apps.fluxgui')

        self._color = self.settings.get_string("colortemp")
        self._autostart = self.settings.get_boolean("autostart")
        self._latitude = self.settings.get_string("latitude")
        self._longitude = self.settings.get_string("longitude")
        self._zipcode = self.settings.get_string("zipcode")

        self.has_set_prefs = True
        if not self._latitude and not self._zipcode:
            self.has_set_prefs = False
            self._zipcode = '90210'
            self.autostart = True

        # After an upgrade to fluxgui where the color options change,
        # the color setting may no longer be one of the menu
        # options. In this case, we reset to the default night time
        # temp.
        if self._color not in temperatures:
            self.color = default_temperature
        else:
            self.color = self._color

    def xflux_settings_dict(self):
        d = {
            'color': self.color,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'zipcode': self.zipcode,
            'pause_color': off_temperature
        }
        return d

    def _get_color(self):
        return self._color

    def _set_color(self, value):
        self._color = value
        self.settings.set_string("colortemp", value)

    def _get_latitude(self):
        return self._latitude

    def _set_latitude(self, value):
        self._latitude = value
        self.settings.set_string("latitude", value)

    def _get_longitude(self):
        return self._longitude

    def _set_longitude(self, value):
        self._longitude = value
        self.settings.set_string("longitude", value)

    def _get_zipcode(self):
        return self._zipcode

    def _set_zipcode(self, value):
        self._zipcode = value
        self.settings.set_string("zipcode", value)

    def _get_autostart(self):
        return self._autostart

    def _set_autostart(self, value):
        self._autostart = value
        self.settings.set_boolean("autostart", self._autostart)
        if self._autostart:
            self._create_autostarter()
        else:
            self._delete_autostarter()

    color = property(_get_color, _set_color)
    latitude = property(_get_latitude, _set_latitude)
    longitude = property(_get_longitude, _set_longitude)
    zipcode = property(_get_zipcode, _set_zipcode)
    autostart = property(_get_autostart, _set_autostart)

    # autostart code copied from AWN

    def _get_autostart_file_path(self):
        autostart_dir = os.path.join(os.environ['HOME'], '.config',
                                     'autostart')
        return os.path.join(autostart_dir, 'fluxgui.desktop')

    def _create_autostarter(self):
        autostart_file = self._get_autostart_file_path()
        autostart_dir = os.path.dirname(autostart_file)

        if not os.path.isdir(autostart_dir):
            # create autostart dir
            try:
                os.mkdir(autostart_dir)
            except DirectoryCreationError as e:
                print("Creation of autostart dir failed, please make it yourself: {}".format(autostart_dir))
                raise e

        if not os.path.isfile(autostart_file):
            # create autostart entry
            starter_item = DesktopEntry(autostart_file)
            starter_item.set('Name', 'f.lux indicator applet')
            # Use the user's shell to start 'fluxgui', in case
            # 'fluxgui' is not installed on a standard system path. We
            # use 'sh' to start the users '/etc/passwd' shell via
            # '$SHELL', so that this will still work if the user
            # changes their shell after the
            # 'autostart/fluxgui.desktop' file is created.
            #
            # See PR #89 for an alternative approach:
            #
            #   https://github.com/xflux-gui/fluxgui/pull/89
            #
            # The escaping of the 'Exec' field is described in
            #
            #   https://developer.gnome.org/desktop-entry-spec/#exec-variables.
            starter_item.set('Exec', r'sh -c "\\"\\$SHELL\\" -c fluxgui"')
            starter_item.set('Icon', 'fluxgui')
            starter_item.set('X-GNOME-Autostart-enabled', 'true')
            starter_item.write()
            self.autostart = True

    def _delete_autostarter(self):
        autostart_file = self._get_autostart_file_path()
        if os.path.isfile(autostart_file):
            os.remove(autostart_file)
            self.autostart = False
