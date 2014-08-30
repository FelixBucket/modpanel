/*****************************
A pusher simulator for testing
the MCP while offline.
*****************************/
define([], function(){

    function Simulator(app_key){
        this.channels = {channels: {}};
        this.subscribe = function(channel){
            this.channels.channels[channel] = new SimulatedChannel(channel);
            return this.channels.channels[channel];
        }
        this.unsubscribe = function(channel){

        }
    }

    function SimulatedChannel(name){
        this.bind = function(event, callback){

        }
    }

    window.Pusher = Simulator;
});