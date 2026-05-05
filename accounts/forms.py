from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from .models import CustomUser
from django import forms
from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "password1", "password2", "is_writer")


# Password Change Form
class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", widget=PasswordInput)
    new_password1 = forms.CharField(label="New Password", widget=PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=PasswordInput)


# Password Reset Form
class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        test = CustomUser.objects.filter(email=email)
        if not test:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


# Password Reset Confirm Form
class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})
    )
