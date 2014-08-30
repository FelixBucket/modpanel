define(['backbone', 'marionette', 'jquery', 'text!./template.html', 'text!./inner_template.html', 'server', 'spin', 'toastr', 'util', 'bootstrap', 'datetimepicker'], function(Backbone, Marionette, $, template, inner_template, server, Spinner, toastr, util){

    var ip_total = 0;

    //Models
    var InfractionSubject = Backbone.Model.extend({
        toggleStatus: function(){
            if (!this.get('included')){
                this.set({included: true, barbed: false});
            }else if (!this.get('barbed')){
                this.set({included: true, barbed: true});
            }else{
                this.set({included: false, barbed: false});
            }
        },
    });
    var SubjectsCollection = Backbone.Collection.extend({
        model: InfractionSubject,
    });

    //Views
    var statusLabel = function(model){
        var status = '<span class="label label-success">Not Included</span>';
        if (model.get('included')){
            if (model.get('barbed')){
                status = '<span class="label label-danger">Barbed</span>';
            }else{
                status = '<span class="label label-warning">Included</span>';
            }
        }
        return status;
    }
    var UsernameView = Marionette.ItemView.extend({
        initialize: function(){
            var _this = this;
            this.$el = $('<tr class="pointer no-highlight"></tr>');
            this.listenTo(this.model, 'change', this.render);
            this.$el.on('click', function(){
                _this.model.toggleStatus();
            });
        },
        render: function(){
            this.$el.html('<td>' + this.model.get('instance').username + '</td><td>' + statusLabel(this.model) + '</td>');
        },
    });
    var IPView = Marionette.ItemView.extend({
        initialize: function(){
            var _this = this;
            this.$el = $('<tr class="pointer no-highlight"></tr>');
            this.listenTo(this.model, 'change', this.render);
            this.$el.on('click', function(){
                _this.model.toggleStatus();
            });
        },
        render: function(){
            this.$el.html('<td>' + this.model.get('identifier') + '</td><td>' + this.model.get('occurances') + '</td><td>' + Math.floor((parseInt(this.model.get('occurances'))/ip_total) * 100) + '%</td><td>' + statusLabel(this.model) + '</td>');
        }
    });

    //Collection Views
    var PartialCollectionView = function(identifier_type, SubviewClass){
        return Backbone.View.extend({
            initialize: function(){
                this.subviews = [];
            },
            render: function(){
                var _this = this;

                //Reset the view
                this.onDestroy();

                //Add all views currently in the collection
                this.collection.each(function(subject){
                    _this.add(subject);
                });

                this.listenTo(this.collection, 'add', this.add);
                this.listenTo(this.collection, 'remove', this.remove);
            },
            add: function(subject){
                if (subject.get('identifier_type') != identifier_type) return;

                var subview = new SubviewClass({model: subject});
                subview.render();
                this.$el.append(subview.$el);

                this.subviews.push(subview);
            },
            remove: function(subject){
                var _this = this;
                //Find the subview
                _.each(this.subviews, function(subview, idx){
                    if (subview.model == subject){
                        subview.destroy();
                        _this.subviews.splice(idx, 1);
                    }
                });
            },
            onDestroy: function(){
                _.each(this.subviews, function(subview){
                    subview.destroy();
                });
                this.$el.empty();
            },
        });
    };
    var UsernamesView = PartialCollectionView('user', UsernameView);
    var IPsView = PartialCollectionView('ip', IPView);

    return Marionette.View.extend({
        constructor: function(infraction_id, initial_usernames, initial_ips){
            if (!initial_usernames) initial_usernames = [];
            if (!initial_ips) initial_ips = [];

            this.infraction_id = infraction_id;
            this.initial_usernames = initial_usernames;
            this.initial_ips = initial_ips;
            Marionette.View.apply(this, null);
        },
        initialize: function(){
            var _this = this;
            this.renderLoading();

            if (this.infraction_id){
                server.get('/api/v1/infractions/' + this.infraction_id + '/')
                .done(function(infractions){
                    if (infractions.length > 0){
                        var infr = infractions[0];

                        _.each(infr.subjects, function(subject){
                            subject.included = true;
                        });

                        infr.subjects = new SubjectsCollection(infr.subjects);
                        _this.infraction = infr;
                        _this.loadIPs();
                    }else{
                        _this.$el.find('.modal').modal('hide');
                        toastr.warning("Something went wrong while loading that infraction.");
                    }
                }).fail(function(){
                    _this.$el.find('.modal').modal('hide');
                    toastr.warning("Something went wrong while loading that infraction.");
                });
            }else{
                //Set up new infraction data
                this.infraction = {
                    external_reason: "",
                    internal_reason: "",
                    expiration: null,

                    change_level: null,
                    speechat_only: false,
                    no_true_firneds: false,
                    no_community_areas: false,

                    subjects: new SubjectsCollection(),
                };

                //Add initial usernames
                _.each(this.initial_usernames, function(username){
                    _this.infraction.subjects.add({
                        identifier_type: 'user',
                        identifier: null,
                        included: true,
                        barbed: false,
                        pricked_by: null,

                        instance: {username: username},
                    });
                });

                //Add initial ips
                _.each(this.initial_ips, function(ip){
                    _this.infraction.subjects.add({
                        identifier_type: 'ip',
                        identifier: ip,
                        included: true,
                        barbed: false,
                        pricked_by: null,
                        occurances: 0,
                    });
                });

                this.loadIPs();
            }
        },
        loadIPs: function(){
            var _this = this;
            var query = "";
            _.each(this.infraction.subjects.where({'identifier_type': 'user'}), function(subject, idx){
                if (idx > 0) query += "&";
                query += 'usernames[]=' + subject.get('instance').username;
            });
            server.get('/api/v1/users/ip_addresses/?' + query).done(function(ips){
                _this.addIPs(ips);
            }).fail(function(){
                _this.render();
            });
        },
        addIPs: function(ips){
            var subjects = this.infraction.subjects;
            _.each(ips, function(ip){
                var existing = subjects.findWhere({'identifier_type': 'ip', 'identifier': ip.ip});
                if (existing){
                    existing.set('occurances', ip.occurances);
                }else{
                    subjects.add({
                        identifier_type: 'ip',
                        identifier: ip.ip,
                        included: false,
                        barbed: false,
                        pricked_by: null,
                        occurances: ip.occurances,
                    });
                }
            });

            this.render();
        },
        renderLoading: function(){
            var _this = this;
            this.$el.html(template);
            this.$el.appendTo($('body'));

            var $el = this.$el.find('.modal-body');
            $el.html('<div class="spinner" style="margin:40px"></div>');
            this.loading_spinner = new Spinner().spin($el.find('.spinner')[0]);

            this.$el.find('.modal').modal().on('hidden.bs.modal', function (e) {
                _this.destroy();
            });
        },
        render: function(){
            var _this = this;
            if (this.loading_spinner) this.loading_spinner.stop();

            var $el = this.$el.find('.modal-body').empty();

            ip_total = 0;
            _.each(this.infraction.subjects.where({'identifier_type': 'ip'}), function(ip){
                ip_total += ip.get('occurances');
            });

            $el.html(_.template(inner_template, {infraction: this.infraction, ip_total: ip_total}));

            $el.find('.backbone-bind').on('change', function(){
                var $input = $(this);

                var prop = $input.data('field');
                var val = $input.val();
                if ($input.prop('type') == 'checkbox') val = $input.prop('checked');

                _this.infraction[prop] = val;
            });

            $el.find('#ei-change-level').on('change', function(){
                var checked = $(this).prop('checked');
                $('#ei-new-level').toggle(checked);
                if (!checked){
                    _this.infraction.change_level = null;
                }else{
                    _this.infraction.change_level = $('#ei-new-level').val();
                }
            });
            $el.find('#ei-new-level').on('change', function(){
                if ($('#ei-change-level').prop('checked')) _this.infraction.change_level = parseInt($(this).val());
            });

            //Datetime picker
            this.$el.find('.datetime-picker').datetimepicker();

            //Subjects
            this.usernames_view = new UsernamesView({collection: this.infraction.subjects, el: this.$el.find('#ei-subjects-usernames')});
            this.ips_view = new IPsView({collection: this.infraction.subjects, el: this.$el.find('#ei-subjects-ips')});
            this.usernames_view.render();
            this.ips_view.render();

            //Finish
            this.$el.find('#acct-infraction-save').click(function(){
                _this.finish();
            });
        },
        finish: function(){
            var _this = this;

            //Copy the infraction data
            var prepared_infraction = $.extend(true, {}, this.infraction);
            prepared_infraction.subjects = [];
            this.infraction.subjects.each(function(subject){
                if (subject.get('included')) prepared_infraction.subjects.push($.extend(true, {}, subject.attributes));
            });

            //Before we send in the infraction, we need to do some validation
            //Check for at least one infraction
            if (prepared_infraction.subjects.length == 0){
                toastr.warning("Well, it helps to have at least one subject of the infraction. Wouldn't you agree?");
                return;
            }

            //Check the expiration date
            if (prepared_infraction.expiration){
                var mysql_datetime = moment(prepared_infraction.expiration).format('YYYY-MM-DD HH:mm:ss');
                if (mysql_datetime == "Invalid date"){
                    toastr.warning("Please enter a valid expiration date, or leave it empty.");
                    return;
                }
                prepared_infraction.expiration = mysql_datetime;
            }

            util.blocker.blockWithSpinner();
            //We need to pull the web_ids of any usernames that we don't have
            _.each(prepared_infraction.subjects, function(subject){
                if (subject.identifier_type == "user" && !subject.identifier){
                    server.get('/api/v1/users/?username=' + subject.instance.username).done(function(accounts){
                        if (accounts.length > 0){
                            subject.identifier = accounts[0].id;
                            _this.continueFinish(prepared_infraction);
                        }else{
                            util.blocker.unblock();
                            toastr.warning("Hmm, I couldn't find an account with the username '" + subject.instance.username + "'!");
                        }
                    }).fail(function(){
                        util.blocker.unblock();
                        toastr.warning("Hmm, I couldn't find an account with the username '" + subject.instance.username + "'!");
                    });
                }
            });
            this.continueFinish(prepared_infraction);
        },
        continueFinish: function(prepared_infraction){
            var _this = this;

            //Check if we have all of the identifiers
            var ready = true;
             _.each(prepared_infraction.subjects, function(subject){
                if (subject.identifier_type == "user" && !subject.identifier) ready = false;
            });
            if (!ready) return;

            //We are ready to submit the infraction to the server
            server.post('/api/v1/infractions/' + (prepared_infraction.id ? prepared_infraction.id + '/' : ''), prepared_infraction, {sendAsJSON: true})
            .done(function(infraction){
                _this.$el.find('.modal').modal('hide');
                _this.trigger('finish', infraction);
            }).always(function(){
                util.blocker.unblock();
            });
        },
    });
});