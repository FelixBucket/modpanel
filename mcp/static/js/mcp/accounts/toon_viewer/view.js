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

            //Back to accounts
            this.$el.find('#back_to_accounts').click(function(e){
                e.preventDefault();
                app.router.navigate('accounts/', {trigger: true});
            });

            //Back to accounts
            this.$el.find('#back_to_account').click(function(e){
                e.preventDefault();
                app.router.navigate('accounts/' + toon.web_id + '/', {trigger: true});
            });

            //Revoke a toon name (badname)
            this.$el.find('#revoke-name').click(function(e){
                e.preventDefault();
                _this.revokeName(toon);
            });
        },
        revokeName: function(toon){
            var _this = this;

            var $btn = this.$el.find('#revoke-name');
            $btn.attr('disabled', true);

            server.post('/api/v1/toons/' + toon.id + '/badname/').done(function(){
                $btn.removeClass('btn-danger').addClass('btn-primary').html('<i class="fa fa-check"></i> Name Revoked!');

                //Load their new name
                server.get('/api/v1/toons/' + toon.id + '/').done(function(toon){
                    _this.$el.find('#toon-name').text(toon.name);
                });
            }).fail(function(){
                $btn.attr('disabled', false);
            });
        },
        onDestroy: function(){
        },
    });
});