# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ProfileTable

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

# accounts/forms.py


# accounts/forms.py

class SignUpForm(UserCreationForm):
    class Meta:
        model = ProfileTable
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_pic', 'phone_number']  # Include first_name and last_name

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.user_type = 'user'  # Set user_type to 'user' by default
        if commit:
            user.save()
        return user