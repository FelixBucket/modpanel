define(['app', './view'], function(app, SidebarView){
    app.module('sidebar', function(sidebar, app){

        sidebar.addInitializer(function(){
            this.view = new SidebarView();
            app.sidebarRegion.show(this.view);
        });

    });
});