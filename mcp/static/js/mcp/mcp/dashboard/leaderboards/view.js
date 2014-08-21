define(['app', 'marionette', 'underscore', 'text!./template.html', 'server', 'util', 'scrollbar', 'morris'], function(app, Marionette, underscore, template, server, util){
    return Marionette.View.extend({
        constructor: function(){
            var _this = this;
            Marionette.View.apply(this, arguments);

            this.leaderboards = {};
            this.render();
            this.mode = 'daily';
            this.loadLeaders();
        },
        render: function(board){
            var _this = this;
            this.mode = board;

            this.$el.html(_.template(template, {
                mode: this.mode,
                static: util.static,
                leaders: this.leaderboards[board],
            }));

            util.scrollbars.start(this.$el.find('.leaderboard-runners-up'), 247);

            //Leaderboard toggles
            this.$el.find('.leaderboard-toggles > a').click(function(e){
                e.preventDefault();
                _this.render($(this).data('mode'));
            });
        },
        loadLeaders: function(){
            var _this = this;
            server.get('/api/v1/leaderboards/').done(function(leaderboards){
                _this.leaderboards = leaderboards;
                var entry = _this.leaderboards['daily'][0];
                _this.leaderboards['daily'] = [entry, entry, entry, entry, entry, entry,entry, entry, entry, entry, entry, entry];
                _this.render(_this.mode);
            });
        },
    });
});