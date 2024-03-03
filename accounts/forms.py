from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        fields = ['phone_number', 'birth_date', 'image']
