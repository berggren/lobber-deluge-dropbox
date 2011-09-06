/*
Script: lobberdropbox.js
    The client-side javascript code for the LobberDropbox plugin.
*/

LobberDropboxPlugin = Ext.extend(Deluge.Plugin, {
    constructor: function(config) {
        config = Ext.apply({
            name: "LobberDropbox"
        }, config);
        LobberDropboxPlugin.superclass.constructor.call(this, config);
    },

    onDisable: function() {

    },

    onEnable: function() {

    }
});
new LobberDropboxPlugin();
