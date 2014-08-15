define(['app', 'marionette', 'util', 'text!./template.html', './stats/view', 'text!./bulletins/template.html', 'bootbox', 'server', 'slimscroll', 'livestamp', 'clamp'], function(app, Marionette, util, template, StatsView, bulletin_template, bootbox, server){

    var bulletins = util.collections.readyFactory('bulletins');
    bulletins.fetch();

    var BulletinView = Marionette.ItemView.extend({
        template: util.views.templateFactory(bulletin_template),
        onRender: function(){
            $clamp(this.$el.find('.text')[0], {clamp: 3});
        },
        events: {
            'click': 'view',
        },
        modelEvents: {
            'change': 'render'
        },
        view: function(){
            server.get('/api/v1/bulletins/' + this.model.get('id'));
            this.model.set('unread', false);
            bootbox.alert('<h4>' + this.model.get('title') + '</h4><p class="text-muted">Posted by ' + this.model.get('author').long_name + '</p>' + this.model.get('content'));
        }
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