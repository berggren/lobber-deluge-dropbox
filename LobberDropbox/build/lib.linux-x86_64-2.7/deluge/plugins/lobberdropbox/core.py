import logging
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export
import os
from pprint import pformat
from twisted.internet.task import LoopingCall
from deluge.maketorrent import TorrentMetadata
import base64
import time
from deluge.ui.client import client

DEFAULT_PREFS = {
    "test":"foo"
}

log = logging.getLogger(__name__)

class DropboxWatcher:
    def __init__(self, dropbox, register=True, acl=None, publicAccess=False, move=True):
        self.dropbox = dropbox
        self.register = register
        self.acl = acl
        self.publicAccess = publicAccess
        self.move = move

    def kill_torrent(self):
        pass

    def make_torrent(self, data_path, torrent_path):
        torrent = TorrentMetadata()
        torrent.data_path = data_path
        torrent.trackers = [["http://127.0.0.1:7000/tracker/uannounce"]]
        torrent.save(torrent_path)

    def start_torrent(self, torrent_file_name):
        torrent_b64 = base64.b64encode(open(torrent_file_name, 'r').read())
        torrent_id = component.get("Core").add_torrent_file(torrent_file_name, torrent_b64, {})
        return torrent_id
    
    def watch_dropbox(self):
        try:
            for file_name in os.listdir(self.dropbox):
                torrent_file_name = "%s%s%s.torrent" % (self.dropbox,os.sep,file_name)
                data_file_name = "%s%s%s" % (self.dropbox, os.sep, file_name)
                if not file_name.endswith(".torrent") and not os.path.exists(torrent_file_name):
                    log.info("Found new file: %s" % data_file_name)
                    while True:
                        if time.time() - os.stat(data_file_name).st_mtime > 10:
                            log.info("%s is done writing, moving on." % data_file_name)
                            break
                        else:
                            log.info("%s is still written to, waiting.." % data_file_name)
                            time.sleep(5)
                    self.make_torrent(data_file_name, torrent_file_name)
                    log.info("Created torrent %s of %s" % (torrent_file_name, data_file_name))
                    self.start_torrent(torrent_file_name)
        except Exception, err:
            log.error(err)
            raise

class Core(CorePluginBase):
    def enable(self):
        self.config = deluge.configmanager.ConfigManager("lobberdropbox.conf", DEFAULT_PREFS)
        self.dropboxwatcher = DropboxWatcher(dropbox="/tmp/dropbox")
        self.dropbox = LoopingCall(self.dropboxwatcher.watch_dropbox)
        self.dropbox.start(5)
        log.info("Lobber dropbox plugin started")
        client.lobberdropbox.testus()

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
