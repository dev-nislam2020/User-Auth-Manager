from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView

from profiles.forms import ContactForm, ProfileForm
from profiles.models import Profile


# Create your views here.
class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'profiles/profile.html'
    
    def get_object(self, queryset=None):
        return Profile.objects.filter(user=self.request.user).first()

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    login_url ='users:login'
    form_class = ProfileForm
    template_name = 'profiles/update.html'
    success_url = reverse_lazy('profiles:profile')
    
    
    def get_form_kwargs(self):
        kwargs = super(UserProfileUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_object(self, queryset=None):
        user_info = Profile.objects.filter(user=self.request.user).first()
        return user_info

class ContactView(FormView):
    template_name = 'profiles/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
