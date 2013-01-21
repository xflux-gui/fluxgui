import gconf

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

    def get_client_bool(self, property_name, default=False):
        client_bool = self.client.get_bool(self.prefs_key+"/"+property_name)
        if client_bool is None:
            client_bool = default
        return client_bool

    def set_client_bool(self, property_name, value):
        self.client.set_bool(self.prefs_key + "/" + property_name, bool(value))


