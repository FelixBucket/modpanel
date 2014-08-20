define(['app', 'marionette', 'util', 'text!./template.html', 'server', 'typeahead'], function(app, Marionette, util, template, server){

    return Marionette.View.extend({
        initialize: function(){
        },
        render: function(){
            var _this = this;
            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT}));

            var accounts = new Bloodhound({
                datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                remote: '/api/v1/find_accounts/%QUERY/'
            });

            accounts.initialize();

            this.$el.find('.typeahead').typeahead(null, {
                displayKey: 'username',
                source: accounts.ttAdapter()
            }).on('typeahead:selected', function(e, account){
                app.router.navigate('accounts/' + account.id + '/', {trigger: true});
            });
        },
        onDestroy: function(){

        }
    });
});