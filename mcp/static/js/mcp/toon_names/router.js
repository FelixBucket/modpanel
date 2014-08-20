define(['backbone', 'app', './view', 'backbone.subroute'], function(Backbone, app, ToonNamesView){
    return Backbone.SubRoute.extend({
        routes: {
            "": "launchView",
        },
        launchView: function() {
            var view = new ToonNamesView();
            app.swapView(view);
            app.setTitle('Approve Names');
            app.router.updateSidebarApp('name_approval');
        },
    });
});