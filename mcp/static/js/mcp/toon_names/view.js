define(['app', 'marionette', 'util', 'text!./template.html', 'text!./name_template.html', 'server'], function(app, Marionette, util, template, comment_template, server){

    //Bulletin Definitions
    comments = util.collections.readyFactory('news_item_comments');

    var loadMoreComments = function(){
        console.log("Loading more");
        server.get('/api/v1/news_item_comments/?approved=false').done(function(loaded){
            comments.set(loaded);
        });
    };

    var CommentView = Marionette.ItemView.extend({
        template: util.views.templateFactory(comment_template),
        events: {
            'click .approve': 'approve',
            'click .reject': 'reject',
        },
        approve: function(){
            this.moderate(1);
        },
        reject: function(){
            this.moderate(0);
        },
        moderate: function(approve){
            server.post('/api/v1/news_item_comments/' + this.model.get('id') + '/moderate/', {approve: approve});
            var collection = this.model.collection;
            collection.remove(this.model);
            if (collection.length == 0) loadMoreComments();
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
            loadMoreComments();
            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT}));

            var CommentCollectionView =  Marionette.CollectionView.extend({
                collection: comments,
                childView: CommentView,
                emptyView: EmptyView,
                initialize: function(){
                    this.render();
                }
            });

            this.commentsView = new CommentCollectionView({el: this.$el.find('#moderation-comments')});
        },
        onDestroy: function(){
            this.commentsView.destroy();
        }
    });
});