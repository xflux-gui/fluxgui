import os
import gconf
from xdg.DesktopEntry import DesktopEntry
from fluxgui.exceptions import DirectoryCreationError


class Settings(object):

    def __init__(self):
        self.client = GConfClient("/apps/fluxgui")

        self._color = self.client.get_client_string("colortemp", 3400)
        self._autostart = self.client.get_client_bool("autostart")
        self._latitude = self.client.get_client_string("latitude")
        self._longitude = self.client.get_client_string("longitude")
        self._zipcode = self.client.get_client_string("zipcode")

        self.has_set_prefs = True
        if not self.latitude and not self.zipcode:
            self.has_set_prefs = False
            self._zipcode = '90210'
            self.autostart=True
        if not self.color:
            self.color = '3400'

    def xflux_settings_dict(self):
        d = {
                'color': self.color,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'zipcode': self.zipcode,
                'pause_color': '6500'
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
            starter_item.set('Exec', 'fluxgui')
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

