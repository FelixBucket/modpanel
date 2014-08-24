define(['app', 'marionette', 'util', 'text!./template.html', 'server', 'util'], function(app, Marionette, util, template, server, util){

    return Marionette.View.extend({
        constructor: function(avatar_id){
            this.avatar_id = avatar_id;
            Marionette.View.apply(this, null);
        },
        render: function(){
            var _this = this;
            this.$el.html('<div class="row"><div class="col-md-12"><p><strong><i class="fa fa-spinner fa-spin"></i> Just a sec while I pull that up...</strong></p></div></div>');

            server.get('/api/v1/toons/' + this.avatar_id + '/').done(function(toon){
                _this.renderToon(toon);
            }).fail(function(){
                _this.$el.html('<div class="row"><div class="col-md-12"><p><strong><i class="fa fa-warning"></i> I couldn\'t find that toon!</strong></p></div></div>')
            });
        },
        renderToon: function(toon){
            var _this = this;

            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT, toon: toon, util: util}));
        },
        onDestroy: function(){
        },
    });
});