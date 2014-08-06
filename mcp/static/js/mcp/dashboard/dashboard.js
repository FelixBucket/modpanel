define(['app', 'marionette', './view'], function(app, Marionette, DashboardView){
    return Marionette.Controller.extend({
        initialize: function(){
            this.view = new DashboardView();
            app.mainRegion.show(this.view);
            app.setTitle('Dashboard');
        },
        onClose: function(){
            this.view.close();
        }
    });
});