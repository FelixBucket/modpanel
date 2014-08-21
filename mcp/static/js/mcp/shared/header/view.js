define(['app', 'marionette', 'text!./template.html', 'jquery', 'util'], function(app, Marionette, template, $, util){
    return Marionette.View.extend({
        render: function(){
            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT, user: app.user, util: util}));

            var $search = this.$el.find('.mobile-search');
            $search.click(function(e) {
                e.preventDefault();

                $search.addClass('active');
                $search.find('form input.form-control').focus();
            });
            $(document).mouseup(function (e) {
                if (!$search.is(e.target) // if the target of the click isn't the container...
                    && $search.has(e.target).length === 0) // ... nor a descendant of the container
                {
                    $search.removeClass('active');
                }
            });
        }
    });
});