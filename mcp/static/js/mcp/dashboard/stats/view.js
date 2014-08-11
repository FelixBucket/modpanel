define(['app', 'marionette', 'underscore', 'text!./template.html', 'server'], function(app, Marionette, underscore, template, server){
    return Marionette.View.extend({
        constructor: function(){
            var _this = this;
            Marionette.View.apply(this, arguments);

            this.render();
            this.loadStats();
        },
        render: function(){
            var _this = this;
            this.$el.html(template);
        },
        loadStats: function(){
            var _this = this;
            server.get('/api/v1/dashboard_stats/').done(function(stats){
                _this.updateStats(stats);
            });
        },
        updateStats: function(stats){
            this.$el.find('#ds-accounts').text(stats.accounts);
            this.$el.find('#ds-playtimes').text(stats.playtimes);
            this.$el.find('#ds-actions-today').text(stats.actions_today);
            this.$el.find('#ds-total-actions').text(stats.total_actions);
        }
    });
});