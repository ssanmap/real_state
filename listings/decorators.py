from django.http import HttpResponseForbidden

def user_is_landlord(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.userprofile.user_type.name == 'arrendador':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not allowed to access this page.")
    return _wrapped_view
