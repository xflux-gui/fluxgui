import gconf

class GConfClient(object):

    def __init__(self):
        self.client = gconf.client_get_default()
        self.prefs_key = "/apps/fluxgui"
        self.client.add_dir(self.prefs_key, gconf.CLIENT_PRELOAD_NONE)

    def get_client_string(self,propertyName,default=""):
        clientString=self.client.get_string(self.prefs_key+"/"+propertyName)
        if clientString is None:
            clientString = str(default)
        return clientString

    def set_client_string(self,propertyName,value):
        self.client.set_string(self.prefs_key + "/" + propertyName, str(value))


