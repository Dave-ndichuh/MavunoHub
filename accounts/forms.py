#signup form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import UserProfile


class SignupForm(UserCreationForm):
    USER_TYPES = [
        ('farmer', 'Farmer'),
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create a UserProfile for this user
            UserProfile.objects.create(user=user, user_type=self.cleaned_data['user_type'])
        return user

#login form

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

