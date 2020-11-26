from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='auth/login.html'),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(),
        name='change_password',
    ),
    path(
        'change-password-done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done',
    ),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'password-reset/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
]