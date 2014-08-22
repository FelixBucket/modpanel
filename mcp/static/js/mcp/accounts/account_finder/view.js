define(['app', 'marionette', 'util', 'text!./template.html', 'server', 'bootbox', 'typeahead'], function(app, Marionette, util, template, server, bootbox){

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

            //Highlight the typeahead field immediately
            setTimeout(function(){
                _this.$el.find('.typeahead').focus();
            }, 50);

            //Add callbacks for the direct fields
            this.$el.find('#goto-webid').on('keyup', function(e){
                if (e.keyCode == 13){
                    var val = $(this).val();
                    if (val){
                        app.router.navigate('accounts/' + val + '/', {trigger: true});
                    }
                }
            });

            this.$el.find('#goto-username').on('keyup', function(e){
                if (e.keyCode == 13){
                    var val = $(this).val();
                    if (val){
                        var input = $(this);
                        input.prop('disabled', true);
                        $.get('/api/v1/users/?username=' + val).always(function(){
                            input.prop('disabled', false);
                        }).done(function(response){
                            if (response.length == 1){
                                app.router.navigate('accounts/' + response[0].id + '/', {trigger: true});
                            }else{
                                bootbox.alert("Hmm, I couldn't find an account with that username.");
                            }
                        }).fail(function(){
                             bootbox.alert("Hmm, I couldn't find an account with that username.");
                        });
                    }
                }
            });
        },
        onDestroy: function(){

        }
    });
});