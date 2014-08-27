requirejs.config({
    paths: {
        jquery: '../../lib/jquery-2.1.1.min',
        underscore: '../../lib/lodash.underscore.min',
        'underscore-string': '../../lib/underscore.string',
        bootstrap: '../../lib/bootstrap.min',
        backbone: '../../lib/backbone-min',
        marionette: '../../lib/backbone.marionette.min',
        'backbone.subroute': '../../lib/backbone.subroute.min',
        moment: '../../lib/moment.min',
        livestamp: '../../lib/livestamp.min',
        bootbox: '../../lib/bootbox.min',
        toastr: '../../lib/toastr.min',
        mousewheel: '../../lib/jquery.mousewheel.min',
        scrollbar: '../../lib/perfect-scrollbar.min',
        clamp: '../../lib/clamp.min',
        hotkeys: '../../lib/jquery.hotkeys',
        'bootstrap-wysiwyg': '../../lib/bootstrap-wysiwyg',
        'pusher-lib': '//js.pusher.com/2.2/pusher.min',
        raphael: '../../lib/raphael-min',
        morris: '../../lib/morris.min',
        typeahead: '../../lib/typeahead.bundle.min',
        md5: '../../lib/md5',
        konami: '../../lib/konami',

        server: 'shared/services/server',
        util: 'shared/services/util',
        pusher: 'shared/services/pusher',
        modal: 'shared/modal/modal',
    },
    shim: {
        bootstrap: ['jquery'],
        underscore: {
            exports: '_',
        },
        'underscore-string': ['underscore'],
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone',
        },
        marionette: {
            deps: ['backbone'],
            exports: 'Marionette',
        },
        'backbone.subroute': ['backbone'],
        moment: {
            exports: 'moment',
        },
        livestamp: ['moment'],
        bootbox:{
            deps:['jquery', 'bootstrap'],
            exports: 'bootbox',
        },
        'bootstrap-wysiwyg': ['jquery', 'bootstrap', 'hotkeys'],
        morris: ['jquery', 'raphael'],
        typeahead: ['jquery'],
        scrollbar: ['mousewheel'],
        konami: ['jquery'],
    },
});

require(['app', 'domReady'], function(app){
    app.start();
});