define(['app', 'marionette', 'text!./template.html', 'jquery'], function(app, Marionette, template, $){
    return Marionette.View.extend({
        render: function(){
            this.$el.html(_.template(template, {STATIC_ROOT: window.STATIC_ROOT}));

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