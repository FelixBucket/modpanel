define(['app', 'backbone', 'marionette', 'underscore'], function(app, Backbone, Marionette, _){

    app.collection_classes = {};
    app.model_classes = {};

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
                return _.template(template, serialized_data);
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

    return {
        collections: collections,
        models: models,
        views: views,
    }

});