requirejs.config({
    //urlArgs: "bust=v1",
    paths: {
        jquery: '../../lib/jquery-2.1.1.min',
        underscore: '../../lib/lodash.underscore.min',
        'underscore-string': '../../lib/underscore.string',
        bootstrap: '../../lib/bootstrap.min',
        backbone: '../../lib/backbone-min',
        marionette: '../../lib/backbone.marionette.min',
        moment: '../../lib/moment.min',
        bootbox: '../../lib/bootbox.min',
        toastr: '../../lib/toastr.min',
        nanoscroller: '../../lib/jquery.nanoscroller.min',
        slimscroll: '../../lib/jquery.slimscroll.min',
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
        moment: {
            exports: 'moment',
        },
        bootbox:{
            deps:['jquery', 'bootstrap'],
            exports: 'bootbox',
        },
    },
});

require(['app', 'domReady'], function(app){
    app.start();
});