from setuptools import setup, find_packages

__plugin_name__ = "LobberDropbox"
__author__ = "Johan Berggren"
__author_email__ = "jbn@nordu.net"
__version__ = "0.1"
__url__ = ""
__license__ = "GPLv3"
__description__ = ""
__long_description__ = """"""
__pkg_data__ = {"deluge.plugins."+__plugin_name__.lower(): ["template/*", "data/*"]}

setup(
    name=__plugin_name__,
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    long_description=__long_description__ if __long_description__ else __description__,

    packages=find_packages(),
    namespace_packages = ["deluge", "deluge.plugins"],
    package_data = __pkg_data__,

    entry_points="""
    [deluge.plugin.core]
    %(plugin_name)s = deluge.plugins.%(plugin_module)s:CorePlugin
    [deluge.plugin.gtkui]
    %(plugin_name)s = deluge.plugins.%(plugin_module)s:GtkUIPlugin
    [deluge.plugin.web]
    %(plugin_name)s = deluge.plugins.%(plugin_module)s:WebUIPlugin
    """ % dict(plugin_name=__plugin_name__, plugin_module=__plugin_name__.lower())
)
