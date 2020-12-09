from django.contrib.auth import views as auth_views
from django.urls import path

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
        auth_views.PasswordChangeView.as_view(
            template_name='auth/password_change_form.html'
        ),
        name='change_password',
    ),
    path(
        'change-password-done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='auth/password_change_done.html'
        ),
        name='password_change_done',
    ),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='auth/password_reset_form.html'
        ),
        name='password_reset',
    ),
    path(
        'password-reset/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='auth/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
]
