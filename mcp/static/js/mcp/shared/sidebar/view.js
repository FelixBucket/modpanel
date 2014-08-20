define(['app', 'marionette', 'text!./template.html', 'jquery', 'bootbox'], function(app, Marionette, template, $, bootbox){
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

            this.listenTo(app.router, 'sidebar_change', this.updateHighlightedRoute);
            this.updateHighlightedRoute();

            this.listenTo(app.pending_counts, 'change', this.updateCounts);
            this.updateCounts();

            this.$el.find('#sidebar-items > li > a').click(function(e){
                e.preventDefault();
                if ($(this).data('route') == null){
                    bootbox.alert("Whoa there cowboy, that's not ready yet! Check back soon!");
                    return;
                }
                app.router.navigate($(this).data('route'), {trigger: true});
            });
        },
        updateCounts: function(){
            var emptyIfZero = function(val){
                if (!val || val == 0) return "";
                return val;
            }

            this.$el.find('#sidebar-ct-toon-names').text(emptyIfZero(app.pending_counts.get('toon_names')));
            this.$el.find('#sidebar-ct-comments').text(emptyIfZero(app.pending_counts.get('comments')));
        },
        updateHighlightedRoute: function(){
            var app_name = app.router.currentSidebarApp;
            this.$el.find('#sidebar-items > li').removeClass('active');
            this.$el.find('#sidebar-items > li[data-app="' + app_name + '"]').addClass('active');
        },
    });
});