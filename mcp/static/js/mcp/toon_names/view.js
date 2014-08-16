define(['app', 'marionette', 'util', 'text!./template.html', 'text!./name_template.html', 'server', 'bootbox'], function(app, Marionette, util, template, name_template, server, bootbox){

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
            this.$el.find('.moderation-name').addClass('done');
            app.pending_counts.set('toon_names', app.pending_counts.get('toon_names')-1);
            server.post('/api/v1/toon_names/' + this.model.get('id') + '/moderate/', {approve: approve});
            var collection = this.model.collection;
            this.model.set('processed', true);  //Yes I know this isn't a realistic value, but it doesn't matter
            if (collection.where({processed: null}) == 0) loadMoreNames();
        }
    });

    var EmptyView = Marionette.ItemView.extend({
        template: function(){
            return '<div class="row"><div class="col-md-12 text-center"><h4>Well, that\'s all of them for now! Good job!</h4></div></div>';
        }
    });

    return Marionette.View.extend({
        render: function(){
            var _this = this;
            loadMoreNames();
            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT}));

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
        onDestroy: function(){
            this.namesView.destroy();
        }
    });
});