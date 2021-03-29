from django.urls import path

from users.views import (RegisterView, UserActivate, UserHomeView,
                         UserLoginView, UserLogoutView, UserPasswordChangeView,
                         UserPasswordResetConfirmView, UserPasswordResetView,
                         UserRegisterView)

# Create your urls here.
app_name = 'users'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('home/', UserHomeView.as_view(), name='home'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('password/change/', UserPasswordChangeView.as_view(), name='password-change'),
    path('password/reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('password/reset/confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    path('register/activate/', RegisterView.as_view(), name='register-activate'),
    path('activate/<uidb64>/<token>/', UserActivate.as_view(), name='activate'),  
]
