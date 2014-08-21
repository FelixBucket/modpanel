define(['app', 'backbone', 'marionette', 'underscore', 'md5', 'scrollbar'], function(app, Backbone, Marionette, _){

    app.collection_classes = {};
    app.model_classes = {};

    var staticUtil = {
        pathForUserAvatar: function(img, email){
            if (!img){
                if (!email){
                    return app.STATIC_ROOT + 'img/mcp/default_avatar.png';
                }else{
                    //Use gravatar if we don't have an image on file but have an email address
                    var default_avatar = encodeURIComponent('http://cp.toontownrewritten.com' + app.STATIC_ROOT + 'img/mcp/default_avatar.png');
                    return "http://www.gravatar.com/avatar/" + CryptoJS.MD5(email).toString() + "?s=150&d=" + default_avatar;
                }
            }else{
                //TODO: Point to AWS eventually for toon images
                return "";
            }
        }
    };

    var models = {
        factory: function(name){

            if (app.model_classes[name]) return app.model_classes[name];

            var ModelClass = Backbone.Model.extend({
            });

            app.model_classes[name] = ModelClass;
            return ModelClass;
        },
        readyFactory: function(name, constructor_options){
            var ModelClass = this.factory(name);
            return new ModelClass(constructor_options);
        },
    };

    var collections = {
        factory: function(resource, model){

            if (app.collection_classes[resource]) return app.collection_classes[resource];

            if (!model) model = models.factory(resource);

            var CollectionClass = Backbone.Collection.extend({
                model: model,
                url: app.api(resource),
            });

            app.collection_classes[resource] = CollectionClass;
            return CollectionClass;
        },
        readyFactory: function(resource, model, constructor_options){
            var CollectionClass = this.factory(resource, model);
            return new CollectionClass(constructor_options);
        },
    };

    var views = {
        templateFactory: function(template){
            return function(serialized_data){
                return _.template(template, $.extend(serialized_data, {
                    SITE_ROOT: app.SITE_ROOT,
                    STATIC_ROOT: app.STATIC_ROOT,
                    active_user: app.user,
                    static: staticUtil,
                }));
            }
        },

        collectionViewFactory: function(collection, childView){
            return Marionette.CollectionView.extend({
                collection: collection,
                childView: childView,
            });
        },
        readyCollectionViewFactory: function(collection, childView, constructor_options){
            var CollectionViewClass = this.collectionViewFactory(collection, childView);
            return new CollectionViewClass(constructor_options);
        }
    };

    var scrollbars = {
        start: function($el, height, width, options){
            if (height) $el.height(height);
            if (width) $el.width(width);

            $el.css('position', 'relative').css('overflow', 'hidden');

            setTimeout(function(){
                $el.perfectScrollbar();
            }, 100);
        },
    };

    return {
        static: staticUtil,
        collections: collections,
        models: models,
        views: views,
        scrollbars: scrollbars,
    }

});