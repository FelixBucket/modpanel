define(['backbone', 'marionette', 'router', 'pusher', 'jquery', 'toastr', 'bootstrap', 'underscore-string'], function(Backbone, Marionette, Router, pusher, $, toastr){
    //Prepare underscore mixins
    _.mixin(_.string.exports());

    //Configure toastr
    toastr.options.newestOnTop = false;

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

    app.activeView = false;
    app.pageTitle = "";

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
        //Connect to pusher
        pusher.startWithAppKey(window.PUSHER_KEY_ID);

        //Initialize and start the router
        app.router = new Router();
        Backbone.history.start({pushState: false, root: window.SITE_ROOT});

        //Initialize Header and Sidebar
        require(['shared/header/header', 'shared/sidebar/sidebar']);

        //Subscribe to pusher for pending_counts
        var counts_channel = pusher.subscribe('pending_counts');
        counts_channel.bind('change', function(new_counts){
            app.pending_counts.set(new_counts);
        });
    });

    app.setTitle = function(title){
        app.pageTitle = title;
        app.updateTitle();
    }
    app.updateTitle = function(){
        var title = app.pageTitle + ' | Toontown Rewritten MCP';

        //Tally up counts
        var sum = 0;
        _.each(app.pending_counts.attributes, function(c){
            sum += c;
        });
        if (sum > 0) title = "(" + sum + ") " + title;

        document.title = title;
    }

    app.api = function(resource){
        return app.SITE_ROOT + 'api/v1/' + resource;
    }

    app.swapView = function(view){
        if (app.activeView) app.activeView.destroy();
        app.activeView = view;
        app.mainRegion.show(app.activeView);
    }

    //Model for pending counts
    var PendingCountsModel = Backbone.Model.extend({
        url: '/api/v1/pending_counts/',
        increment: function(prop){
            if (!isNaN(this.get(prop))) this.set(prop, this.get(prop) + 1);
        },
        decrement: function(prop){
            if (this.get(prop) > 0) this.set(prop, this.get(prop) - 1);
        },
    });
    app.pending_counts = new PendingCountsModel();
    app.pending_counts.on('change', app.updateTitle);
    app.pending_counts.fetch();

    //For now, update the pending counts every minute. Eventually this will all be done through pusher.
    setInterval(function(){
        app.pending_counts.fetch();
    }, 60000);

    app.SITE_ROOT = window.SITE_ROOT;
    app.STATIC_ROOT = window.STATIC_ROOT;
    app.user = $.extend(window.USER, {
        permissions: window.USER_PERMISSIONS,
        hasPermission: function(perm){
            return app.user.permissions.indexOf(perm) > -1;
        },
    });

    return app;
});