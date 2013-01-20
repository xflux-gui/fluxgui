import gconf

class GConfClient(object):

    def __init__(self,prefs_key):
        self.client = gconf.client_get_default()
        self.prefs_key = prefs_key
        self.client.add_dir(self.prefs_key, gconf.CLIENT_PRELOAD_NONE)

    def get_client_string(self,propertyName,default=""):
        clientString=self.client.get_string(self.prefs_key+"/"+propertyName)
        if clientString is None:
            clientString = default
        return clientString

    def set_client_string(self,propertyName,value):
        self.client.set_string(self.prefs_key + "/" + propertyName, str(value))

    def get_client_bool(self, propertyName, default=False):
        clientBool=self.client.get_bool(self.prefs_key+"/"+propertyName)
        if clientBool is None:
            clientBool=default
        return clientBool

    def set_client_bool(self,propertyName,value):
        self.client.set_bool(self.prefs_key + "/" + propertyName, bool(value))


