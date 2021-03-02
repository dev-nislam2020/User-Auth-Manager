from django.urls import path

from profiles.views import UserProfileView, UserProfileUpdateView

# Create your urls here.
app_name = 'profiles'
urlpatterns = [
    path('', UserProfileView.as_view(), name='profile'),
    path('update/', UserProfileUpdateView.as_view(), name='profile-update'),
]
