define(['app', 'marionette', 'util', 'text!./template.html', 'text!./name_template.html', 'server', 'bootbox', 'pusher', 'text!./guidelines.html', 'modal'], function(app, Marionette, util, template, name_template, server, bootbox, pusher, guidelines, Modal){

    names = util.collections.readyFactory('news_item_comments');

    var loadMoreNames = function(){
        server.get('/api/v1/toon_names/?processed=None').done(function(loaded){
            names.push(loaded);
        });
    };

    var NameView = Marionette.ItemView.extend({
        template: util.views.templateFactory(name_template),
        events: {
            'click .approve': 'approve',
            'click .reject': 'reject',
            'click .discuss': 'discuss',
        },
        modelEvents:{
            'moderated_remotely': 'moderated_remotely',
        },
        approve: function(){
            if (this.model.get('processed')) return;
            this.$el.find('.approve').addClass('selected').html('<i class="fa fa-check"></i><p>Approved</p><p>' + this.model.get('candidate_name') + '</p>');
            this.$el.find('.reject, .discuss').addClass('not-selected');
            this.moderate(1);
        },
        reject: function(){
            if (this.model.get('processed')) return;
            this.$el.find('.reject').addClass('selected').html('<i class="fa fa-times"></i><p>Rejected</p><p>' + this.model.get('candidate_name') + '</p>');
            this.$el.find('.approve, .discuss').addClass('not-selected');
            this.moderate(0);
        },
        discuss: function(){
            if (this.model.get('processed')) return;
            bootbox.alert("Whoa there cowboy, you can't discuss Toon Names yet. You'll be able to soon!");
        },
        moderate: function(approve){
            var _this = this;

            this.$el.find('.moderation-name').addClass('done');
            if (app.pending_counts.get('toon_names') >= 1) {
                app.pending_counts.set('toon_names', app.pending_counts.get('toon_names')-1);
            }

            var collection = this.model.collection;
            this.model.set('processed', true);  //Yes I know this isn't a realistic value, but it doesn't matter

            server.post('/api/v1/toon_names/' + this.model.get('id') + '/moderate/', {approve: approve})
            .done(function(){
                if (collection.where({processed: undefined}) == 0) loadMoreNames();
            }).fail(function(){
                _this.model.set('processed', false);
                app.pending_counts.set('toon_names', app.pending_counts.get('toon_names')+1);
                _this.render();
            });
        },
        moderated_remotely: function(approve, moderator){
            this.$el.find('.moderation-name').addClass('done');
            if (app.pending_counts.get('toon_names') >= 1) {
                app.pending_counts.set('toon_names', app.pending_counts.get('toon_names')-1);
            }

            if (approve){
                this.$el.find('.approve').addClass('selected').html('<i class="fa fa-check"></i><p>Approved by ' + moderator + '</p><p>' + this.model.get('candidate_name') + '</p>');
                this.$el.find('.reject, .discuss').addClass('not-selected');
            }else{
                this.$el.find('.reject').addClass('selected').html('<i class="fa fa-times"></i><p>Rejected by ' + moderator + '</p><p>' + this.model.get('candidate_name') + '</p>');
                this.$el.find('.approve, .discuss').addClass('not-selected');
            }

            var collection = this.model.collection;
            this.model.set('processed', true);  //Yes I know this isn't a realistic value, but it doesn't matter
            if (collection.where({processed: undefined}) == 0) loadMoreNames();
        }
    });

    var EmptyView = Marionette.ItemView.extend({
        template: function(){
            return '<div class="row"><div class="col-md-12 text-center"><h4>Well, that\'s all of them for now! Good job!</h4></div></div>';
        }
    });

    return Marionette.View.extend({
        initialize: function(){
            this.channel = pusher.subscribe('toon_names');
            this.channel.bind('moderated', this.remoteModeration, this);
        },
        render: function(){
            var _this = this;
            loadMoreNames();
            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT}));

            this.$el.find('#tn-approval-guidelines').click(function(){
                new Modal(guidelines);
            });

            var NameCollectionView =  Marionette.CollectionView.extend({
                collection: names,
                childView: NameView,
                emptyView: EmptyView,
                initialize: function(){
                    this.render();
                }
            });

            this.namesView = new NameCollectionView({el: this.$el.find('#moderation-names')});
        },
        remoteModeration: function(payload){
            //A name has been moderated by someone else (or potentially us), let's see if we have it loaded
            var name = names.findWhere({id: payload.toon_name_id});

            //If we don't have it loaded or have already moderated it ourselves, ignore it
            if (!name || name.get('processed')) return;

            //Notify the name view by triggering the model's event
            name.trigger('moderated_remotely', payload.approve, payload.moderator);
        },
        onDestroy: function(){
            pusher.unsubscribe('toon_names');
            this.namesView.destroy();
        }
    });
});