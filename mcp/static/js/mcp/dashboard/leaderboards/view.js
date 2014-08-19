define(['app', 'marionette', 'underscore', 'text!./template.html', 'server', 'util', 'morris'], function(app, Marionette, underscore, template, server, util){
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

                /*** Remove before pushing ***/
                var entry = function(name, points){
                    return {points: points, user: { avatar: "", mini_name: name}};
                }
                _this.leaderboards = {
                    daily: [entry('Nicole E.', 9001), entry('Luke S.', 9000), entry('Eric G.', 10), entry('Lisosaurus', -2), entry('CHRIS Else', -10)],
                    weekly: [entry('Luke S.', 9002), entry('Nicole E.', 4500), entry('Eric G.', 69), entry('Lisosaurus', -2), entry('Someone Else', -10)],
                    all_time: [entry('Nicole E.', 15000), entry('Luke S.', 12000), entry('Badminton G.', 10), entry('Lisosaurus', -2), entry('Someone Else', -10)],
                }
                /*** End remove before pushing ***/

                _this.render(_this.mode);
            });
        },
    });
});