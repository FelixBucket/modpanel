define(['backbone'], function(Backbone){

    var routers = {};

    return Backbone.Router.extend({
        currentSidebarApp: "",
        updateSidebarApp: function(app){
            this.currentSidebarApp = app;
            this.trigger('sidebar_change', this.currentSidebarApp);
        },

        routes: {
            "name_approval/*subroute"  : "invokeNameApprovalApp",
            "comment_approval/*subroute" : "invokeCommentApprovalApp",
            "*subroute"  : "invokePanelApp"
        },
        invokeNameApprovalApp: function(subroute) {
            if (routers.name_approval) return;
            require(['toon_names/router'], function(AppRouter){
                routers.name_approval = new AppRouter("name_approval/", {createTrailingSlashRoutes: true});
            });
        },
        invokeCommentApprovalApp: function(subroute) {
            if (routers.comment_approval) return;
            require(['news_comments/router'], function(AppRouter){
                routers.comment_approval = new AppRouter("comment_approval/", {createTrailingSlashRoutes: true});
            });
        },
        invokePanelApp: function(subroute) {
            if (routers.panel) return;
            require(['mcp/router'], function(AppRouter){
                routers.panel = new AppRouter("", {createTrailingSlashRoutes: true});
            });
        },
    });
});