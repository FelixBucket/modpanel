define(['backbone', 'app', './view', 'backbone.subroute'], function(Backbone, app, NewsCommentsView){
    return Backbone.SubRoute.extend({
        routes: {
            "": "launchView",
        },
        launchView: function() {
            var view = new NewsCommentsView();
            app.swapView(view);
            app.setTitle('Approve Comments');
            app.router.updateSidebarApp('comment_approval');
        },
    });
});