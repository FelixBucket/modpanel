define(['app', 'marionette', './view'], function(app, Marionette, NewsCommentsView){
    return Marionette.Controller.extend({
        initialize: function(){
            this.view = new NewsCommentsView();
            app.mainRegion.show(this.view);
            app.setTitle('Approve Comments');
        },
        onDestroy: function(){
            this.view.destroy();
        }
    });
});