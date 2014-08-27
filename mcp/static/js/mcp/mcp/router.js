define(['backbone', 'app', './dashboard/view', 'backbone.subroute'], function(Backbone, app, DashboardView){
    return Backbone.SubRoute.extend({
        routes: {
            "": "launchView",
        },
        launchView: function() {
            var view = new DashboardView();
            app.swapView(view);
            app.setTitle('Dashboard');
            app.router.updateSidebarApp('dashboard');
        },
    });
});