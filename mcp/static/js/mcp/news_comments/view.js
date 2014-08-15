define(['app', 'marionette', 'util', 'text!./template.html'], function(app, Marionette, util, template){

    return Marionette.View.extend({
        render: function(){
            var _this = this;
            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT}));
        },
        onDestroy: function(){

        }
    });
});