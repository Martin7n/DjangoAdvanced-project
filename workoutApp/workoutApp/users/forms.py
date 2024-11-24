

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from workoutApp.users.models import CustomUser, UserProfile


class CustomLoginForm(AuthenticationForm):
    # You can add custom fields or override validation here
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)




class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # first_name = forms.CharField(max_length=20, required=False)
    # last_name = forms.CharField(max_length=20, required=False)
    # profile_picture = forms.ImageField(required=False)  # Optional profile picture
    # trainer = forms.BooleanField(required=False)  # Optional trainer field

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        # fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture', 'trainer')




class CustomUserChangeForm(UserChangeForm):
    # Fields you want to allow users to edit
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    # profile_picture = forms.ImageField(required=False)
    # trainer = forms.BooleanField(required=False)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '(leave blank to keep current)', 'autocomplete': 'new-password'}),
        label='Change your password (Leave blank to keep the current password)',
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture',]

        profile_picture = forms.ImageField(required=False)