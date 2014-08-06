define(['backbone'], function(Backbone){
    return Backbone.Router.extend({
        routes: {
            '*actions': 'dashboard/dashboard',
        },
    });
});