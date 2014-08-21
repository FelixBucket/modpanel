define(['app', 'marionette', 'util', 'text!./template.html', 'text!./comment_template.html', 'server', 'pusher'], function(app, Marionette, util, template, comment_template, server, pusher){

    var comments;

    var loadMoreComments = function(){
        server.get('/api/v1/news_item_comments/?approved=false').done(function(loaded){
            comments.push(loaded);
        });
    };

    var CommentView = Marionette.ItemView.extend({
        template: util.views.templateFactory(comment_template),
        events: {
            'click .approve': 'approve',
            'click .reject': 'reject',
        },
        modelEvents:{
            'moderated_remotely': 'moderated_remotely',
        },
        approve: function(){
            if (this.model.get('processed')) return;
            this.$el.find('.approve').addClass('selected').html('<i class="fa fa-check"></i><p>Approved</p>');
            this.$el.find('.reject, .discuss').addClass('not-selected');
            this.moderate(1);
        },
        reject: function(){
            if (this.model.get('processed')) return;
            this.$el.find('.reject').addClass('selected').html('<i class="fa fa-times"></i><p>Rejected</p>');
            this.$el.find('.approve, .discuss').addClass('not-selected');
            this.moderate(0);
        },
        moderate: function(approve){
            var _this = this;

            this.$el.find('.moderation-comment').addClass('done');

            var collection = this.model.collection;
            this.model.set('processed', true);  //Yes I know this isn't a realistic value, but it doesn't matter

            server.post('/api/v1/news_item_comments/' + this.model.get('id') + '/moderate/', {approve: approve})
            .done(function(){
                if (collection.where({processed: undefined}) == 0) loadMoreComments();
            }).fail(function(){
                _this.model.set('processed', false);
                app.pending_counts.increment('comments');
                _this.render();
            });
        },
        moderated_remotely: function(approve, moderator){
            this.$el.find('.moderation-comment').addClass('done');
            app.pending_counts.decrement('comments');

            if (approve){
                this.$el.find('.approve').addClass('selected').html('<i class="fa fa-check"></i><p>Approved by ' + moderator + '</p>');
                this.$el.find('.reject, .discuss').addClass('not-selected');
            }else{
                this.$el.find('.reject').addClass('selected').html('<i class="fa fa-times"></i><p>Rejected by ' + moderator + '</p>');
                this.$el.find('.approve, .discuss').addClass('not-selected');
            }

            var collection = this.model.collection;
            this.model.set('processed', true);  //Yes I know this isn't a realistic value, but it doesn't matter
            if (collection.where({processed: undefined}) == 0) loadMoreComments();
        }
    });

    var EmptyView = Marionette.ItemView.extend({
        template: function(){
            return '<div class="row"><div class="col-md-12 text-center"><h4>Well, that\'s all of them for now! Good job!</h4></div></div>';
        }
    });

    return Marionette.View.extend({
        initialize: function(){
            comments = util.collections.readyFactory('news_item_comments');
            this.channel = pusher.subscribe('news_comments');
            this.channel.bind('moderated', this.remoteModeration, this);
        },
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
        remoteModeration: function(payload){
            //A comment has been moderated by someone else (or potentially us), let's see if we have it loaded
            var comment = comments.findWhere({id: payload.comment_id});

            //If we don't have it loaded or have already moderated it ourselves, ignore it
            if (!comment || comment.get('processed')) return;

            //Notify the comment view by triggering the model's event
            comment.trigger('moderated_remotely', payload.approve, payload.moderator);
        },
        onDestroy: function(){
            pusher.unsubscribe('news_comments');
            this.commentsView.destroy();
        }
    });
});