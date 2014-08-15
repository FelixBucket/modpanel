define(['app', 'marionette', 'underscore', 'text!./template.html', 'jquery', 'toastr', 'bootstrap', 'bootstrap-wysiwyg'], function(app, Marionette, _, template, $, toastr){
    return Marionette.View.extend({
        constructor: function(title, initial_entry, use_title){
            this.context = {title: title, initial_entry: (initial_entry ? initial_entry : ''), use_title: use_title};
            this.use_title = use_title;
            Marionette.View.apply(this, null);
        },
        initialize: function(){
            this.render();
        },
        render: function(){
            var _this = this;
            var $el = this.$el;
            $el.html(_.template(template, this.context));
            $el.appendTo($('body'));

            $el.find('.finish-post').on('click', function(){
                _this.finish($el.find('.wysiwyg-editor').cleanHtml(), $el.find('.wysiwyg-title').val());
            });

            $el.find('.modal').modal();

            var fonts = ['Serif', 'Sans', 'Arial', 'Arial Black', 'Courier',
                        'Courier New', 'Comic Sans MS', 'Helvetica', 'Impact', 'Lucida Grande', 'Lucida Sans', 'Tahoma', 'Times',
                        'Times New Roman', 'Verdana'],
            fontTarget = this.$el.find('[title=Font]').siblings('.dropdown-menu');

            $.each(fonts, function (idx, fontName) {
                fontTarget.append($('<li><a data-edit="fontName ' + fontName +'" style="font-family:\''+ fontName +'\'">'+fontName + '</a></li>'));
            });
            this.$el.find('a[title]').tooltip({container:'body'});
            this.$el.find('.dropdown-menu input').click(function() {return false;})
                .change(function () {$(this).parent('.dropdown-menu').siblings('.dropdown-toggle').dropdown('toggle');})
                .keydown('esc', function () {this.value='';$(this).change();});
            this.$el.find('.wysiwyg-editor').wysiwyg();

            setTimeout(function(){
                var $entry = $el.find(_this.use_title ? '.wysiwyg-title' : '.wysiwyg-editor');
                var len = $entry.val().length;
                $entry.focus();
            }, 500);
        },
        finish: function(val, title_val){
            var _this = this;

            if (this.use_title && (!title_val || title_val.length == 0)){
                toastr.warning("You should probably enter a title.");
                return;
            }

            if (!val || val.length == 0){
                toastr.warning("You should probably write something.");
                return;
            }

            this.trigger('finish', val, title_val);
            this.$el.find('.modal').modal('hide').on('hidden.bs.modal', function (e) {
                _this.destroy();
            });
        }
    });
});