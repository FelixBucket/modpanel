define(['app', 'marionette', 'text!./template.html', 'slimscroll'], function(app, Marionette, template){
    return Marionette.View.extend({
        render: function(){
            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT}));

            /** TEMPORARY **/
            /* This logic will be moved into individual widgets */
            //Bulletins Widget
            this.$el.find('.bulletins-inner').slimScroll({
                height: '391px',
                alwaysVisible: false,
                railVisible: true,
                wheelStep: 6,
                allowPageScroll: false
            });

            //Recent Activity Widget
            this.$el.find('.activity-inner').slimScroll({
                height: '400px',
                alwaysVisible: false,
                railVisible: true,
                wheelStep: 6,
                allowPageScroll: false
            });
        }
    });
});