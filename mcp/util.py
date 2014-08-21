from .permissions import permissions
from ttr import api
from ttr.models import *
from ttr.util import send_pusher_message

def require_permission(permission):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs) :

            if request.user.level >= permissions[permission]:
                return view_method(request, *args, **kwargs)
            else:
                return api.error(403)

        return _arguments_wrapper

    return _method_wrapper

def get_pending_counts():
    toon_names_count = ToonName.objects.filter(processed=None).count()
    comments_count = NewsItemComment.objects.filter(approved=False).count()
    return dict(toon_names=toon_names_count, comments=comments_count)

def broadcast_pending_counts():
    send_pusher_message('pending_counts', 'change', get_pending_counts())