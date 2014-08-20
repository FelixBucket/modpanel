define(['app', 'marionette', 'util', 'text!./template.html', 'server'], function(app, Marionette, util, template, server){

    return Marionette.View.extend({
        constructor: function(account_id){
            this.account_id = account_id;
            Marionette.View.apply(this, null);
        },
        render: function(){
            var _this = this;
            this.$el.html('<div class="row"><div class="col-md-12"><p><strong><i class="fa fa-spinner fa-spin"></i> Just a sec while I pull that up...</strong></p></div></div>');

            server.get('/api/v1/accounts/' + this.account_id + '/').done(function(account){
                _this.renderAccount(account);
            });
        },
        renderAccount: function(account){

            //Add in the species for now
            var types = {
                d: 'Dog',
                c: 'Cat',
                m: 'Mouse',
                r: 'Rabbit',
                f: 'Duck',
                p: 'Monkey',
                b: 'Bear',
                s: 'Pig',
            };

            _.each(account.toons, function(toon){
                toon.species = types[toon.headType.substr(0,1)];
            });

            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT, account: account}));
        },
    });
});