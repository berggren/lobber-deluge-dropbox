import logging
from deluge.ui.client import client
from deluge import component
from deluge.plugins.pluginbase import WebPluginBase

from common import get_resource

log = logging.getLogger(__name__)

class WebUI(WebPluginBase):

    scripts = [get_resource("lobberdropbox.js")]

    def enable(self):
        pass

    def disable(self):
        pass
