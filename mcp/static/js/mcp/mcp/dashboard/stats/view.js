define(['app', 'marionette', 'underscore', 'text!./template.html', 'server', 'morris'], function(app, Marionette, underscore, template, server){
    return Marionette.View.extend({
        constructor: function(){
            var _this = this;
            Marionette.View.apply(this, arguments);

            this.render();
            this.loadStats();
            this.loadPopulation();
        },
        render: function(){
            var _this = this;
            this.$el.html(template);

            this.$el.find('.graph-toggles > a').click(function(e){
                e.preventDefault();
                _this.$el.find('.graph-toggles > a').removeClass('active');
                $(this).addClass('active');
                _this.loadPopulation();
            });

            this.graph = Morris.Line({
                element: this.$el.find('#ds-population-graph')[0],
                data: [],
                lineColors: ['#ffffff'],
                xkey: 'timestamp',
                ykeys: ['population'],
                labels: ['Population'],
                pointSize: 0,
                hideHover: 'auto',
                gridTextColor: '#ffffff',
                gridLineColor: 'rgba(255, 255, 255, 0.3)',
                resize: true
            });
        },
        loadStats: function(){
            var _this = this;
            server.get('/api/v1/dashboard_stats/').done(function(stats){
                _this.updateStats(stats);
            });
        },
        updateStats: function(stats){
            this.$el.find('#ds-accounts').text(_.numberFormat(stats.accounts));
            this.$el.find('#ds-playtimes').text(_.numberFormat(stats.playtimes));
            this.$el.find('#ds-actions-today').text(_.numberFormat(stats.actions_today));
            this.$el.find('#ds-total-actions').text(_.numberFormat(stats.total_actions));
        },
        loadPopulation: function(){
            var _this = this;
            var days = this.$el.find('.graph-toggles > a.active').data('days');
            server.get('/api/v1/population_history/?days=' + days).done(function(pop){
                _this.updatePopulation(pop);
            });
        },
        updatePopulation: function(pop){
            _.each(pop, function(p){
                p.timestamp *= 1000;
            });

            this.graph.setData(pop);

            var peak = _.max(_.pluck(pop, 'population'));

            if (!pop[0]) return;
            this.$el.find('#ds-population-now').text(_.numberFormat(pop[0].population));
            this.$el.find('#ds-population-peak').text(_.numberFormat(peak));
        },
    });
});