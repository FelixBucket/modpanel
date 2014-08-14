define(['app', 'marionette', 'util', 'text!./template.html', './stats/view', 'text!./bulletins/template.html', 'slimscroll', 'livestamp'], function(app, Marionette, util, template, StatsView, bulletin_template){

    var bulletins = util.collections.readyFactory('bulletins');
    bulletins.fetch();

    var BulletinView = Marionette.ItemView.extend({
        template: util.views.templateFactory(bulletin_template),
    });

    return Marionette.View.extend({
        render: function(){
            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT}));

            //Stats
            this.stats_view = new StatsView({el: this.$el.find('#dashboard-stats')});

            //Bulletins Widget
            this.bulletins_view = util.views.readyCollectionViewFactory(bulletins, BulletinView, {el: this.$el.find('#bulletins-list')});
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
        },
        destroy: function(){
            this.stats_view.destroy();
        }
    });
});