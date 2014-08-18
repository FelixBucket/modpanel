requirejs.config({
    paths: {
        jquery: '../../lib/jquery-2.1.1.min',
        underscore: '../../lib/lodash.underscore.min',
        toastr: '../../lib/toastr.min',

        server: 'shared/services/server',
    },
    shim: {
        underscore: {
            exports: '_',
        },
    },
});

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

var displayMessage = function(message, type){
    if (!message){
        $('.alert').hide();
        return;
    }

    if (!type) type = "warning";

    $('.alert')
        .removeClass('alert-warning')
        .removeClass('alert-danger')
        .removeClass('alert-success')
        .addClass('alert-' + type)
        .text(message)
        .show();
}

var login = function(server, username, password, remember_me){
    displayMessage();
    $('#login-form *').prop('disabled', true);
    server.post('/api/v1/login/', {
        username: username,
        password: password,
        remember_me: remember_me ? 1 : 0,
    }, {verbose: false, splash: false}).always(function(){
        $('#login-form *').prop('disabled', false);
    }).done(function(response){
        if (response.status == 'tfa'){
            $('#login-form').hide();
            $('#login-form-2fa').show();
            window.login_data = response;
        }else{
            window.location.href = '/';
        }
    }).fail(function(raw){
        var response = raw.responseJSON;
        displayMessage(response.error);
    });
}

var login2fa = function(server, token){
    displayMessage();
    $('#login-form-2fa *').prop('disabled', true);
    server.post('/api/v1/login/', {
        tfa_userid: window.login_data.tfa_userid,
        tfa_signature: window.login_data.tfa_signature,
        tfa_token: token,
    }, {verbose: false, splash: false}).always(function(){
        $('#login-form-2fa *').prop('disabled', false);
    }).done(function(response){
        window.location.href = '/';
    }).fail(function(raw){
        var response = raw.responseJSON;
        displayMessage(response.error);
    });
}

require(['jquery', 'underscore', 'server'], function($, _, server){
    prepareCSRFToken();

    window.login_data = {};

    $('#login-form button').click(function(e){
        e.preventDefault();
        login(server, $('#username').val(), $('#password').val(), $('#remember-me').val() == "on");
    });

    $('#login-form-2fa button').click(function(e){
        e.preventDefault();
        login2fa(server, $('#token').val());
    });
});