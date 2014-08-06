define(['app', './view'], function(app, HeaderView){
    app.module('header', function(header, app){

        header.addInitializer(function(){
            this.view = new HeaderView();
            app.headerRegion.show(this.view);
        });

    });
});