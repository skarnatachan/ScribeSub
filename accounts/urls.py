from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .forms import PwdResetForm, PwdResetConfirmForm

app_name = "accounts"

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("my-login/", views.my_login, name="my-login"),
    path('user-logout/', views.user_logout, name='user-logout'),
    # ── Password Change Zone ──────────────────────────────────────────────────
    path('password-change/', views.password_change, name='password-change'),
    path('password-change/done/', views.password_change_done, name='password-change-done'),
    # ── Password Reset Zone ──────────────────────────────────────────────────
    # Step 1: User submits their email
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/registration/password_reset_form.html',
             email_template_name='accounts/registration/password_reset_email.html',
             form_class=PwdResetForm,
             success_url=reverse_lazy('accounts:password_reset_done')  # → step 2
         ),
         name='password-reset'),

    # Step 2: "Check your inbox" confirmation page
    path('password-reset/email-sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    # Step 3: User clicks link in email → sets new password
    # NOTE: Django expects the parameter name 'uidb64' (not 'uid64')
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/registration/password_reset_confirm.html',
             form_class=PwdResetConfirmForm,
             success_url=reverse_lazy('accounts:password_reset_complete')  # → step 4
         ),
         name='password_reset_confirm'),

    # Step 4: Success page after password has been reset
    path('password-reset/success/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
