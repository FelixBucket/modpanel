define(['backbone', 'marionette', 'jquery', 'text!./template.html', 'server', 'spin', 'toastr', 'util', '../infraction_editor/infraction_editor', 'bootstrap'], function(Backbone, Marionette, $, template, server, Spinner, toastr, util, InfractionEditor){

    return Marionette.View.extend({
        constructor: function(account){
            this.account = account;
            Marionette.View.apply(this, null);
        },
        initialize: function(){
            var _this = this;
            viewer = this;

            this.renderLoading();
            server.get('/api/v1/users/' + this.account.id + '/infractions/').done(function(infractions){
                _this.infractions = infractions;
                _this.render();
            }).fail(function(){
                _this.$el.find('.modal').modal('hide');
            });
        },
        renderLoading: function(){
            var _this = this;
            this.$el.html(_.template(template, {account: this.account}));
            this.$el.appendTo($('body'));

            var $el = this.$el.find('.modal-body');
            $el.html('<div class="spinner" style="margin:40px"></div>');
            this.loading_spinner = new Spinner().spin($el.find('.spinner')[0]);

            this.$el.find('.modal').modal().on('hidden.bs.modal', function (e) {
                _this.destroy();
            });

            this.$el.find('#ai-add-another').click(function(){
                _this.$el.find('.modal').modal('hide');
                var editor = new InfractionEditor(null, [_this.account.username]);
            });
        },
        render: function(){
            var _this = this;

            var $el = this.$el.find('.modal-body').html('<table class="table table-responsive table-hover table-compact"><thead><th>External Reason</th><th>Internal Reason</th><th>Expiration</th></thead><tbody></tbody></table>');
            var $body = $el.find('tbody');

            var prettyDate = function(date){
                if (!date){
                    return '<span class="text-muted">Permanent</span>';
                }
                return moment(date).format('MM/DD/YYYY h:mm A');
            }

            _.each(this.infractions, function(infraction){
                var $tr = $('<tr class="pointer no-highlight"><td> ' + infraction.external_reason + '</td><td>' + infraction.internal_reason + '</td><td>' + prettyDate(infraction.expiration) + '</td>');
                $tr.on('click', function(){
                    _this.editInfraction(infraction.id);
                });
                $body.append($tr);
            });
        },
        editInfraction: function(id){
            this.$el.find('.modal').modal('hide');
            var editor = new InfractionEditor(id);
        },
    });
});