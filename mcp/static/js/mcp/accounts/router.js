define(['backbone', 'app', './account_finder/view', './account_viewer/view', 'backbone.subroute'], function(Backbone, app, AccountFinderView, AccountViewerView){
    return Backbone.SubRoute.extend({
        routes: {
            ""                  : "launchAccountFinder",
            ":account_id/"      : "launchAccountView",
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
    });
});