define(['app', './view'], function(app, SidebarView){
    app.module('sidebar', function(sidebar, app){

        sidebar.addInitializer(function(){
            sidebar.view = new SidebarView();
            app.sidebarRegion.show(sidebar.view);
        });

    });
});