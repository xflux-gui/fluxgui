import os
import gconf
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
    '2000', # The minimum supported by flux; see https://github.com/xflux-gui/xflux-gui/issues/51
    '2300',
    '2700',
    '3400', # The 'default_temperature' needs to be one of the options!
    '4200',
    '5000',
    # The "off temperature" is not one of the menu choices, but
    # the previous code included it, so @ntc2 is leaving it in
    # without understanding why ...
    #
    # TODO(ntc2): understand why this entry is in the list, and remove
    # it if possible.
    off_temperature ]

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
        # You can use 'gconftool --dump /apps/fluxgui' to see current
        # settings on command line.
        self.client = GConfClient("/apps/fluxgui")

        self._color = self.client.get_client_string("colortemp", 3400)
        self._autostart = self.client.get_client_bool("autostart")
        self._latitude = self.client.get_client_string("latitude")
        self._longitude = self.client.get_client_string("longitude")
        self._zipcode = self.client.get_client_string("zipcode")

        self.has_set_prefs = True
        if not self._latitude and not self._zipcode:
            self.has_set_prefs = False
            self._zipcode = '90210'
            self.autostart=True

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
        return str(self._color)
    def _set_color(self, value):
        self._color = value
        self.client.set_client_string("colortemp", value)

    def _get_latitude(self):
        return str(self._latitude)
    def _set_latitude(self, value):
        self._latitude = value
        self.client.set_client_string("latitude", value)

    def _get_longitude(self):
        return str(self._longitude)
    def _set_longitude(self, value):
        self._longitude = value
        self.client.set_client_string("longitude", value)

    def _get_zipcode(self):
        return str(self._zipcode)
    def _set_zipcode(self, value):
        self._zipcode = value
        self.client.set_client_string("zipcode", value)

    def _get_autostart(self):
        return bool(self._autostart)
    def _set_autostart(self, value):
        self._autostart = value
        self.client.set_client_bool("autostart", self._autostart)
        if self._autostart:
            self._create_autostarter()
        else:
            self._delete_autostarter()

    color=property(_get_color, _set_color)
    latitude=property(_get_latitude, _set_latitude)
    longitude=property(_get_longitude, _set_longitude)
    zipcode=property(_get_zipcode, _set_zipcode)
    autostart=property(_get_autostart, _set_autostart)


    #autostart code copied from AWN
    def _get_autostart_file_path(self):
        autostart_dir = os.path.join(os.environ['HOME'], '.config',
                                     'autostart')
        return os.path.join(autostart_dir, 'fluxgui.desktop')

    def _create_autostarter(self):
        autostart_file = self._get_autostart_file_path()
        autostart_dir = os.path.dirname(autostart_file)

        if not os.path.isdir(autostart_dir):
            #create autostart dir
            try:
                os.mkdir(autostart_dir)
            except DirectoryCreationError, e:
                print "Creation of autostart dir failed, please make it yourself: %s" % autostart_dir
                raise e

        if not os.path.isfile(autostart_file):
            #create autostart entry
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

class GConfClient(object):
    """
    Gets and sets gconf settings.
    """

    def __init__(self, prefs_key):
        self.client = gconf.client_get_default()
        self.prefs_key = prefs_key
        self.client.add_dir(self.prefs_key, gconf.CLIENT_PRELOAD_NONE)

    def get_client_string(self, property_name, default=""):
        client_string = self.client.get_string(self.prefs_key+"/"+property_name)
        if client_string is None:
            client_string = default
        return client_string

    def set_client_string(self, property_name, value):
        self.client.set_string(self.prefs_key + "/" + property_name, str(value))

    def get_client_bool(self, property_name, default=True):
        try:
            gconf_type = self.client.get(self.prefs_key + "/"
                                            + property_name).type
        except AttributeError:
            # key is not set
            self.set_client_bool(property_name, default)
            client_bool = default
            return client_bool

        client_bool = None
        if gconf_type != gconf.VALUE_BOOL:
            # previous release used strings for autostart, handle here
            client_string = self.get_client_string(property_name).lower()
            if client_string == '1':
                self.set_client_bool(property_name, True)
                client_bool = True
            elif client_string == '0':
                self.set_client_bool(property_name, False)
                client_bool = False
        else:
            client_bool = self.client.get_bool(self.prefs_key
                                        + "/"+property_name)
        return client_bool

    def set_client_bool(self, property_name, value):
        self.client.set_bool(self.prefs_key + "/" + property_name, bool(value))

