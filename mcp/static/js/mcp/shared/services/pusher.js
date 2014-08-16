define(['pusher-lib'], function(){

    /******************************************************

    This is a quick pusher wrapper I threw together to make
    our lives easier. The main library can be a little
    testy about channels.

    This wrapper works just like memory management does.
    Each call to subscribe acts like an alloc, and each to
    unsubscribe acts like a release. The channel_references
    dictionary keeps track of active allocations. When the
    allocations drop to 0, we call unsubscribe on the actual
    pusher object.

    Calling subscribe will only call subscribe on the main
    library if we don't already have a subscription. It will
    always return the chnnel though.

    *******************************************************/

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
