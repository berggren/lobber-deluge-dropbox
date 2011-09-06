import logging
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export

DEFAULT_PREFS = {
    "test":"NiNiNi"
}

log = logging.getLogger(__name__)

class Core(CorePluginBase):
    def enable(self):
        self.config = deluge.configmanager.ConfigManager("lobberdropbox.conf", DEFAULT_PREFS)

    def disable(self):
        pass

    def update(self):
        pass

    @export
    def set_config(self, config):
        """Sets the config dictionary"""
        for key in config.keys():
            self.config[key] = config[key]
        self.config.save()

    @export
    def get_config(self):
        """Returns the config dictionary"""
        return self.config.config
