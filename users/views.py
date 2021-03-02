from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from users.forms import RegisterForm
from users.mixins import AuthenticatedMixin
from users.tokens import user_activation_token


# Create your views here.
class IndexView(AuthenticatedMixin, TemplateView):
    template_name = 'users/index.html'

class UserHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/home.html'

class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('%s?next=%s' % ('/user/home/', self.request.path))
        self.object = None
        return super().get(request, *args, **kwargs)

class UserLoginView(AuthenticatedMixin, LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('%s?next=%s' % ('/user/login/', self.request.path))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/reset/password_change.html'
    success_url = reverse_lazy('users:login')

class UserPasswordResetView(AuthenticatedMixin, PasswordResetView):
    email_template_name = 'users/reset/password_reset_email.html'
    template_name = 'users/reset/password_reset.html'
    success_url = reverse_lazy('users:login')

class UserPasswordResetConfirmView(AuthenticatedMixin, PasswordResetConfirmView):
    template_name = 'users/reset/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')


class RegisterView(CreateView):
    template_name = 'users/register-activate.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('%s?next=%s' % ('/user/home/', self.request.path))
        self.object = None
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('users:login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False 
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Activate Your User Authentication Manager Account'
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': user_activation_token.make_token(user),
        })
        user.email_user(subject, message)

        return super(RegisterView, self).form_valid(user)


class UserActivate(TemplateView):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user.is_active:
            messages.success(request, ('Your account All ready confirmed.'))
            return redirect('index')


        if user is not None and user_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('users:login')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('index')
