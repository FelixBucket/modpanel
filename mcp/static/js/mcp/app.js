define(['backbone', 'marionette', 'router', 'jquery', 'toastr', 'bootstrap', 'underscore-string'], function(Backbone, Marionette, Router, $, toastr){
    //Prepare underscore mixins
    _.mixin(_.string.exports());

    //Configure toastr
    toastr.options.newestOnTop = false;

    //Private App Methods
    var swapController = function(controller, args){
        var _this = this;
        if (this.activeController) this.activeController.close();
        this.activeController = false;
        this.activeControllerClass = controller;
        this.trigger('viewChange', controller);
        require([controller], function(Controller){
            _this.activeController = new Controller();
        });
    }
    var prepareCSRFToken = function(){
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        function sameOrigin(url) {
            // test that a given url is a same-origin URL
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    }
    prepareCSRFToken();

    //App Definition
    var app = new Marionette.Application();

    app.activeController = false;
    app.activeControllerClass = false;

    app.addRegions({
        headerRegion: '#navbarRegion',
        sidebarRegion: '#nav-col',
        mainRegion: '#content-wrapper',
    });

    app.addInitializer(function(){
        setTimeout(function() {
            $('#content-wrapper > .row').css({
                opacity: 1
            });
        }, 200);

        $("[data-toggle='tooltip']").each(function (index, el) {
            $(el).tooltip({
                placement: $(this).data("placement") || 'top'
            });
        });
    });

    app.on('start', function(){
        //Initialize and start the router
        app.router = new Router();
        app.listenTo(app.router, 'route', swapController);
        Backbone.history.start({pushState: true, root: window.SITE_ROOT});

        //Initialize Header and Sidebar
        require(['shared/header/header', 'shared/sidebar/sidebar']);
    });

    app.setTitle = function(title){
        document.title = title + ' | Toontown Rewritten MCP';
    }

    app.SITE_ROOT = window.SITE_ROOT;
    app.STATIC_ROOT = window.STATIC_ROOT;
    app.user = {
        permissions: window.USER_PERMISSIONS,
        hasPermission: function(perm){
            return app.user.permissions.indexOf(perm) > -1;
        },
    };

    return app;
});