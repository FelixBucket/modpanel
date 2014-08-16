define(['app', './view', 'server', 'backbone'], function(app, SidebarView, server, Backbone){
    app.module('sidebar', function(sidebar, app){

        sidebar.addInitializer(function(){
            var PendingCountsModel = Backbone.Model.extend({
                urlRoot: '/api/v1/pending_counts/',
            });
            app.pending_counts = new PendingCountsModel({
                toon_names: 0,
                comments: 0,
            });

            sidebar.view = new SidebarView();
            app.sidebarRegion.show(sidebar.view);
            app.pending_counts.fetch();
        });

    });
});