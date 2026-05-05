from .models import Article
from django import forms
from accounts.models import CustomUser


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['article2customuser', 'date_posted']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        exclude = ['is_writer', 'is_active', 'is_staff', 'date_joined']
