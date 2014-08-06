define(['app', 'marionette', 'text!./template.html', 'jquery'], function(app, Marionette, template, $){
    return Marionette.View.extend({
        render: function(){
            this.$el.html(_.template(template, {STATIC_ROOT: window.STATIC_ROOT}));

            this.$el.find('#sidebar-nav .dropdown-toggle').click(function (e) {
                e.preventDefault();

                var $item = $(this).parent();

                if (!$item.hasClass('open')) {
                    $item.parent().find('.open .submenu').slideUp('fast');
                    $item.parent().find('.open').toggleClass('open');
                }

                $item.toggleClass('open');

                if ($item.hasClass('open')) {
                    $item.children('.submenu').slideDown('fast');
                }
                else {
                    $item.children('.submenu').slideUp('fast');
                }
            });
        }
    });
});