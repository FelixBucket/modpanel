define(['backbone'], function(Backbone){
    return Backbone.Router.extend({
        routes: {
            'name_approval': 'toon_names/toon_names',
            'comment_approval': 'news_comments/news_comments',
            '*actions': 'dashboard/dashboard',
        },
    });
});