define(['toastr'], function(toastr){
    return {

        //Server Helpers
        tastyPost: function(resource, data, resource_id, method, options){
            var resource_url = '/api/v1/' + resource + '/';
            if (resource_id) resource_url += resource_id + '/';

            //Determine the appropriate method
            if (!method) method = (resource_id ? 'PUT' : 'POST');
            if (!options) options = {};
            options.method = method;
            if (options.sendAsJson !== false) options.sendAsJSON = true;

            return this.post(resource_url, data, options);
        },

        // Returns a Deferred, allowing use of the Deferred interface for callbacks (.done, .fail, .always)
        // Expects you to return a response with the appropriate HTTP Response Code (2XX = success, 4XX or 5XX = failure)
        // If you do not specify an error message on a 4XX or 5XX response, it will attempt to explain it in plain English.
        post: function(url, data, options) {
            var defaults = {
                splash: true,
                verbose: "auto",            //can be "success", "fail", "both", "auto" or false (note: "fail" is errors and .fail)
                formData: false,            //tells rmpost whether the data parameter is a FormData object
                method: "POST",
                sendAsJSON: false,

                messageSuccess: "Done.",
                messageFail: "Something went wrong. Please try again.",

                errorMessages: {
                    0: "You do not appear to have an internet connection.",
                    400: "There was a problem with that request.",
                    401: "You do not have permission to do that.",
                    403: "You do not have permission to do that.",
                    404: "Couldn't find that on the server. You may also be offline.",
                    412: "There was a problem with that request.",
                    413: "The file(s) you uploaded were too large.",
                    500: "The server encountered an error. This isn't your fault, and you can try again.",
                    501: "The server isn't sure how to process that request yet.",
                    503: "The server is down for maintenance, please try again later.",
                }
            }
            var settings = $.extend({}, defaults, options);

            function takeFirstNotEmpty(){
                var args = Array.prototype.slice.call(arguments, 0);
                for (var a = 0; a < args.length; a++){
                    if (args[a]) return args[a];
                }
            }

            var displayMessageForResponse = function(response, success, settings){
                var json;
                try{
                    json = $.parseJSON(response.responseText);
                }catch(e){
                    json = {};
                }
                var text;
                if (success){
                    text = takeFirstNotEmpty(response.message, settings.messageSuccess);
                }else{
                    var errors = "";
                    if (json.errors){
                        $.each(json.errors, function(error_context, error_msg){
                            errors += '<strong>' + error_context + '</strong>: ' + error_msg + '<br>';
                        });
                    }
                    text = takeFirstNotEmpty(json.error, errors, settings.errorMessages[response.status], settings.messageFail);
                }
                var layout = takeFirstNotEmpty(response.message_layout, settings.messageLayout)
                var type = takeFirstNotEmpty(response.message_type, (success?'success':'warning'));
                var timeout = takeFirstNotEmpty(response.message_timeout, settings.messageTimeout);

                if (type == "information"){
                    toastr.info(text);
                }else if (type == "success"){
                    toastr.success(text);
                }else if (type == "warning"){
                    toastr.warning(text);
                }else if (type == "error"){
                    toastr.error(text);
                }
            }

            var deferred = $.Deferred();

            var ajaxParams = {
                type: settings.method,
                url: url,
                data: data,
                dataType: "json",
            };

            if (settings.sendAsJSON){
                ajaxParams.data = JSON.stringify(data);
                ajaxParams.contentType = "application/json";
            }

            if (settings.formData){
                ajaxParams.cache = false;
                ajaxParams.contentType = false;
                ajaxParams.processData = false;
            }

            $.ajax(ajaxParams)
            .done(function(response){
                if (settings.verbose == "success" || settings.verbose == "both" || (settings.verbose == "auto" && response && response.message))
                    displayMessageForResponse(response, true, settings);

                deferred.resolve(response);
            })
            .fail(function(response){
                if (settings.verbose == "fail" || settings.verbose == "both" || settings.verbose == "auto")
                    displayMessageForResponse(response, false, settings);

                deferred.reject(response);
            });

            return deferred;

        },
        get: function(url){
            if (url.charAt(0) == '/') url = url.substr(1);
            url = window.SITE_ROOT + url;
            if (url.charAt(url.length-1) != '/' && url.indexOf('?') == -1) url = url + '/';

            var deferred = $.Deferred();

            $.getJSON(url).done(function(response){
                deferred.resolve(response);
            })
            .fail(function(response){
                deferred.reject(response);
            });

            return deferred;
        },
        put: function(url, data, options){
            return this.post(url, data, $.extend({type: "PUT"}, options));
        },
        delete: function(url, data, options){
            return this.post(url, data, $.extend({type: "DELETE"}, options));
        },
    }
});