define(['app', 'marionette', 'text!./template.html', 'jquery'], function(app, Marionette, template, $){
    return Marionette.View.extend({
        render: function(){
            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT, user: app.user}));

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
        },
        updateCounts: function(counts){
            var emptyIfZero = function(val){
                if (!val || val == 0) return "";
                return val;
            }

            this.$el.find('#sidebar-ct-toon-names').text(emptyIfZero(counts.toon_names));
            this.$el.find('#sidebar-ct-comments').text(emptyIfZero(counts.comments));
        },
    });
});