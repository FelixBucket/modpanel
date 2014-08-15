define(['backbone'], function(Backbone){
    return Backbone.Router.extend({
        routes: {
            'comment_approval': 'news_comments/news_comments',
            '*actions': 'dashboard/dashboard',
        },
    });
});