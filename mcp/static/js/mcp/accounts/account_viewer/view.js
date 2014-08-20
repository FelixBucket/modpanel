define(['app', 'marionette', 'util', 'text!./template.html', 'server'], function(app, Marionette, util, template, server){

    return Marionette.View.extend({
        constructor: function(account_id){
            this.account_id = account_id;
            Marionette.View.apply(this, null);
        },
        render: function(){
            var _this = this;
            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT}));

            server.get('/api/v1/accounts/' + this.account_id + '/');
        },
        onDestroy: function(){

        }
    });
});