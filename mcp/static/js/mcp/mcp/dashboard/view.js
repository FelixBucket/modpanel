define(['app', 'marionette', 'util', 'text!./template.html', './stats/view', './leaderboards/view', 'shared/wysiwygModal/view', 'text!./bulletins/template.html', 'text!./activities/template.html', 'bootbox', 'server', 'livestamp', 'clamp'], function(app, Marionette, util, template, StatsView, LeaderboardsView, WysiwygModal, bulletin_template, activity_template, bootbox, server){

    //Bulletin Definitions
    var bulletins;

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

    //Recent Activity Definition
    var recent_activity;
    var ActivityView = Marionette.ItemView.extend({
        template: util.views.templateFactory(activity_template),
    });

    return Marionette.View.extend({
        initialize: function(){
            bulletins = util.collections.readyFactory('bulletins');
            bulletins.fetch();

            recent_activity = util.collections.readyFactory('action_stories');
            recent_activity.fetch();
        },
        render: function(){
            var _this = this;
            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT}));

            //Stats
            this.stats_view = new StatsView({el: this.$el.find('#dashboard-stats')});

            //Leaderboards
            this.leaderboards_view = new LeaderboardsView({el: this.$el.find('#leaderboards')});

            //Bulletins Widget
            this.bulletins_view = util.views.readyCollectionViewFactory(bulletins, BulletinView, {el: this.$el.find('#bulletins-list')});
            util.scrollbars.start(this.$el.find('.bulletins-content'), 368);

            this.$el.find('#dashboard-new-bulletin-task').click(function(){
                var editor = new WysiwygModal('Post a New Bulletin', '', true);
                _this.listenTo(editor, 'finish', function(entry, title){
                    server.tastyPost('bulletins', {title: title, content: entry}).done(function(new_bulletin){
                        bulletins.unshift(new_bulletin);
                    });
                });
            });

            //Recent Activity Widget
            this.recent_activity_view = util.views.readyCollectionViewFactory(recent_activity, ActivityView, {el: this.$el.find('#activity-list')});
            util.scrollbars.start(this.$el.find('.activity-inner'), 377);
        },
        onDestroy: function(){
            this.stats_view.destroy();
            this.leaderboards_view.destroy();
            this.bulletins_view.destroy();
            this.recent_activity_view.destroy();
        }
    });
});