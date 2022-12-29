from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.RegistrationView.as_view(), name='user_signup'),
    path('login', views.LoginView.as_view(), name='user_login'),
    path('profile', views.ProfileView.as_view(), name='user_profile'),
    path('update_password', views.UpdatePasswordView.as_view(), name='user_update_password'),
]
