import logging
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export
import os
from pprint import pformat

DEFAULT_PREFS = {
    "test":"foo"
}

log = logging.getLogger(__name__)

class DropboxWatcher:
    def __init__(self,dropbox,register=True,acl=None,publicAccess=False,move=True):
        self.dropbox = dropbox
        self.register = register
        self.acl = acl
        self.publicAccess = publicAccess
        self.move = move

    def kill_torrent(self):
        pass

    def start_torrent(self):
        pass

    def watch_dropbox(self):
        try:
            for file_name in os.listdir(self.dropbox):
                torrent_file_name = "%s%s%s.torrent" % (self.dropbox,os.sep,fn)
                data_file_name = "%s%s%s" % (self.dropbox,os.sep,fn)
                log.info("found %s" % dfn)
                if not fn.endswith(".torrent") and not os.path.exists(tfn):
                    log.info("making torrent from %s" % dfn)
                    log.info(pformat(dfn))
                    #ToDo: make_torrent here
                    log.msg("renamed %s to %s" % (torrent_file_name,tfn))
                    shutil.move(torrent_file_name,tfn)
                    #self.start_torrent("",tfn,dfn,self.move)
        except Exception, err:
            log.error(err)
            raise

class Core(CorePluginBase):
    def enable(self):
        self.config = deluge.configmanager.ConfigManager("lobberdropbox.conf", DEFAULT_PREFS)
        dropboxwatcher = DropboxWatcher()
        self.dropbox = LoopingCall(self.dropboxwatcher.watch_dropbox)
        self.dropbox.start(5)
        log.info("Lobber dropbox plugin started")

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
