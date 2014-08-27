define(['backbone', 'app', './account_finder/view', './account_viewer/view', './toon_viewer/view', 'backbone.subroute'], function(Backbone, app, AccountFinderView, AccountViewerView, ToonViewerView){
    return Backbone.SubRoute.extend({
        routes: {
            ""                  : "launchAccountFinder",
            ":account_id/"      : "launchAccountView",
            "toon/:avatar_id/"      : "launchToonView",
        },
        launchAccountFinder: function() {
            var view = new AccountFinderView();
            app.swapView(view);
            app.setTitle('Accounts');
            app.router.updateSidebarApp('accounts');
        },
        launchAccountView: function(account_id){
            var view = new AccountViewerView(account_id);
            app.swapView(view);
            app.setTitle('Account');
            app.router.updateSidebarApp('accounts');
        },
        launchToonView: function(avatar_id){
            var view = new ToonViewerView(avatar_id);
            app.swapView(view);
            app.setTitle('Toon');
            app.router.updateSidebarApp('accounts');
        },
    });
});