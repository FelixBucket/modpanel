define(['app', 'marionette', './view'], function(app, Marionette, ToonNamesView, pusher){
    return Marionette.Controller.extend({
        initialize: function(){
            this.view = new ToonNamesView();
            app.mainRegion.show(this.view);
            app.setTitle('Approve Names');
        },
        onDestroy: function(){
            this.view.destroy();
        }
    });
});