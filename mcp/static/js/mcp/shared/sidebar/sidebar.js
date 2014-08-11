define(['app', './view', 'server'], function(app, SidebarView, server){
    app.module('sidebar', function(sidebar, app){

        sidebar.loadCounts = function(){
            server.get('/api/v1/sidebar_counts/').done(function(counts){
                sidebar.view.updateCounts(counts);
            });
        };

        sidebar.addInitializer(function(){
            sidebar.view = new SidebarView();
            app.sidebarRegion.show(sidebar.view);
            sidebar.loadCounts();
        });

    });
});