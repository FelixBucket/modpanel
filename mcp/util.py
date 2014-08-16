from .permissions import permissions
from ttr import api

def require_permission(permission):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs) :

            if request.user.level >= permissions[permission]:
                return view_method(request, *args, **kwargs)
            else:
                return api.error(403)

        return _arguments_wrapper

    return _method_wrapper