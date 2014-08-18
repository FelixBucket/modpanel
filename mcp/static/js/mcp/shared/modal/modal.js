define(['marionette', 'jquery', 'bootstrap'], function(Marionette, $){
    return Marionette.View.extend({
        constructor: function(html){
            this.html = html;
            Marionette.View.apply(this, null);
        },
        initialize: function(){
            this.render();
        },
        render: function(){
            var _this = this;
            var $el = this.$el;
            $el.html(this.html);
            $el.appendTo($('body'));

            $el.find('.modal').modal().on('hidden.bs.modal', function (e) {
                _this.destroy();
            });
        },
    });
});