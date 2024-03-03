from django.contrib.auth import views as auth_views
from django.urls import path, include, reverse_lazy

from django.views.generic.base import TemplateView

from django_registration.backends.activation import views as registration_views
from accounts import views as users_views
from financial_manager import settings

urlpatterns = [
    path('profile/', users_views.profile, name='profile'),

    path('registration/register/',
         registration_views.RegistrationView.as_view(
             template_name='accounts/registration/register.html',
             email_body_template=settings.ACTIVATION_EMAIL_BODY,
             email_subject_template=settings.ACTIVATION_EMAIL_SUBJECT,
             success_url=reverse_lazy("registration_complete"),
             disallowed_url=reverse_lazy("registration_disallowed"),
         ),
         name='registration_register'),

    path('registration/complete/',
         TemplateView.as_view(template_name='accounts/registration/complete.html'),
         name='registration_complete'),

    path('registration/closed/',
         TemplateView.as_view(template_name='accounts/registration/closed.html'),
         name='registration_disallowed'),

    path('registration/activate/<str:activation_key>/',
         registration_views.ActivationView.as_view(
             template_name='accounts/registration/activation_failed.html',
             success_url=reverse_lazy("registration_activation_complete")
         ),
         name='registration_activate'),

    path('registration/activation/complete/',
         TemplateView.as_view(template_name='accounts/registration/activation_complete.html'),
         name='registration_activation_complete'),


    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),


    path('password-reset/request/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset/request.html'),
         name='password_reset_request'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset/done.html'),
         name='password_reset_done'),

    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset/complete.html'),
         name='password_reset_complete'),

    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset/confirm.html'),
         name='password_reset_confirm'),
]
