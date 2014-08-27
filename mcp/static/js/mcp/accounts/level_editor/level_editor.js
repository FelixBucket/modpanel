define(['marionette', 'jquery', 'text!./template.html', 'server', 'bootstrap'], function(Marionette, $, template, server){
    return Marionette.View.extend({
        constructor: function(level, web_id){
            this.web_id = web_id;
            this.level = level;
            Marionette.View.apply(this, null);
        },
        initialize: function(){
            this.render();
        },
        render: function(){
            var _this = this;
            var $el = this.$el;
            $el.html(template);
            $el.appendTo($('body'));

            $el.find('.modal').modal().on('hidden.bs.modal', function (e) {
                _this.destroy();
            });

            //Fill in the switches based on the passed level
            var base_level = Math.floor(this.level/100) * 100;
            $el.find('input[data-val="' + base_level + '"]').parent().addClass('active');

            var bits = this.level % 100;
            if (bits & parseInt('100', 2)) $el.find('input[name="flag-dev"]').prop('checked', true).parent().addClass('active');
            if (bits & parseInt('010', 2)) $el.find('input[name="flag-qa"]').prop('checked', true).parent().addClass('active');
            if (bits & parseInt('001', 2)) $el.find('input[name="flag-test"]').prop('checked', true).parent().addClass('active');

            //Add change handlers
            this.$el.find('input').parent().on('click', function(){
                setTimeout(function(){
                    _this.$el.find('.new-level').text(_this.buildLevel());
                }, 10);
            });

            //Build the level
            $el.find('.new-level').text(this.buildLevel());

            //Finish handler
            $el.find('#acct-level-save').on('click', function(){
                _this.finish();
            });
        },
        buildLevel: function(){
            //Get the base level
            var base = this.$el.find('#base-levels > .active').find('input').data('val');

            //Add flags/bits
            if (this.$el.find('input[name="flag-dev"]').prop('checked')) base += 4;
            if (this.$el.find('input[name="flag-qa"]').prop('checked')) base += 2;
            if (this.$el.find('input[name="flag-test"]').prop('checked')) base += 1;

            return base;
        },
        finish: function(){
            var _this = this;
            var new_level = this.buildLevel();
            server.post('/api/v1/users/' + this.web_id + '/change_level/', {level: new_level})
            .done(function(){
                _this.trigger('change', new_level);
                _this.$el.find('.modal').modal('hide');
            });
        },
    });
});