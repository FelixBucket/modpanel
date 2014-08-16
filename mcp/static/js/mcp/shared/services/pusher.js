define(['pusher-lib'], function(){

    var connection;
    var channel_references = {};

    return{
        startWithAppKey: function(app_key){
            connection = new Pusher(app_key);
        },
        ensureChannelReferenceCount: function(channel_name){
            if (!channel_references[channel_name]){
                channel_references[channel_name] = 0;
            }
        },
        subscribe: function(channel_name){
            this.ensureChannelReferenceCount(channel_name);
            if (channel_references[channel_name] == 0) connection.subscribe(channel_name);
            channel_references[channel_name] ++;
            return connection.channels.channels[channel_name];
        },
        unsubscribe: function(channel_name){
            this.ensureChannelReferenceCount(channel_name);
            channel_references[channel_name] --;
            if (channel_references[channel_name] == 0) connection.unsubscribe(channel_name);
            if (channel_references[channel_name] < 0) channel_references[channel_name] = 0;
            return channel_references[channel_name];
        },
    }
});