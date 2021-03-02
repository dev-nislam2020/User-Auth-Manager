from django.shortcuts import redirect


# Create your urls here.
class AuthenticatedMixin:
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('%s?next=%s' % ('/user/home/', self.request.path))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
