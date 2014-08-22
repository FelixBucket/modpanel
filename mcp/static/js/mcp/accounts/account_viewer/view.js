define(['app', 'marionette', 'util', 'text!./template.html', 'server', 'util', 'konami'], function(app, Marionette, util, template, server, util){

    return Marionette.View.extend({
        constructor: function(account_id){
            this.account_id = account_id;
            Marionette.View.apply(this, null);
        },
        render: function(){
            var _this = this;
            this.$el.html('<div class="row"><div class="col-md-12"><p><strong><i class="fa fa-spinner fa-spin"></i> Just a sec while I pull that up...</strong></p></div></div>');

            server.get('/api/v1/accounts/' + this.account_id + '/').done(function(account){
                _this.renderAccount(account);
            });
        },
        renderAccount: function(account){
            var _this = this;

            //Preload sounds
            var audio = new Audio();
            this.format = null;

            //Force Mp3 for now
            /*if (audio.canPlayType('audio/ogg')){
                this.format = 'ogg'
            }else */if (audio.canPlayType('audio/mp3')){
                this.format = 'mp3';
            }

            if (this.format){
                new Audio(app.STATIC_ROOT + "sounds/mcp/pick_a_toon/rollover." + this.format);
                new Audio(app.STATIC_ROOT + "sounds/mcp/pick_a_toon/click." + this.format);
            }

            //Add in the species for now
            var types = {
                d: 'Dog',
                c: 'Cat',
                m: 'Mouse',
                r: 'Rabbit',
                h: 'Horse',
                f: 'Duck',
                p: 'Monkey',
                b: 'Bear',
                s: 'Pig',
            };
            _.each(account.toons, function(toon){
                if (toon) toon.species = types[toon.dna.headType.substr(0,1)];
            });

            //Pick a toon styling
            var pat_styles = [
                {background: "252,75,81", rotation: 5},
                {background: "162,221,79", rotation: -9},
                {background: "143,85,231", rotation: 2},
                {background: "63,167,255", rotation: -5},
                {background: "233,96,186", rotation: 3},
                {background: "245,215,65", rotation: -4},
            ];

            this.$el.html(_.template(template, {STATIC_ROOT: app.STATIC_ROOT, account: account, pat_styles: pat_styles, util: util}));

            this.$el.find('.panel-toon').on('mouseenter', function(){
                if (_this.format) new Audio(app.STATIC_ROOT + "sounds/mcp/pick_a_toon/rollover." + _this.format).play();

                var $panel = $(this);
                var bg = pat_styles[$panel.data('idx')].background;
                $panel.find('.panel-heading').css('background-color', 'rgba(' + bg + ', 0.65');
                $panel.find('.panel-body').css('background-color', 'rgba(' + bg + ', 0.2');
            });
            this.$el.find('.panel-toon').on('mouseleave', function(){
                var $panel = $(this);
                var bg = pat_styles[$panel.data('idx')].background;
                $panel.find('.panel-heading').css('background-color', 'rgba(' + bg + ', 0.45');
                $panel.find('.panel-body').css('background-color', 'rgba(' + bg + ', 0.1');
            });
            this.$el.find('.panel-toon').on('click', function(){
                if (_this.format) new Audio(app.STATIC_ROOT + "sounds/mcp/pick_a_toon/click." + _this.format).play();
            });

            //Pick a Toon Music
            window.music = new Audio(app.STATIC_ROOT + 'sounds/mcp/pick_a_toon/music.' + this.format);
            window.music.addEventListener('ended', function() {
                this.currentTime = 0;
                this.play();
            }, false);
            $(window).konami({
                cheat: function(){
                    window.music.pause();
                    window.music.currentTime = 0;
                    window.music.play();
                },
            });
        },
        onDestroy: function(){
        },
    });
});