from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from workoutApp.common_utils.workout_choices import ExrxCategory, ExrxType
from workoutApp.users.models import CustomUser, UserProfile
from workoutApp.workouts.models import Exercise


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

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
        widget=forms.PasswordInput(
            attrs={'placeholder': '(leave blank to keep current)',
                   'autocomplete': 'new-password'}),
        label='Change your password (Leave blank to keep the current password)',
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', ]

        profile_picture = forms.ImageField(required=False)


class ExerciseFilterForm(forms.Form):
    EXERCISE_CATEGORY_CHOICES = ExrxCategory.choices
    EXERCISE_TYPE_CHOICES = ExrxType.choices

    exercise_category = forms.ChoiceField(
        choices=[('', 'All Categories')] + list(EXERCISE_CATEGORY_CHOICES),
        required=False,
        label="exercise_category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    exercise_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(EXERCISE_TYPE_CHOICES),
        required=False,
        label="exercise_type",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    exercise_names = forms.ModelChoiceField(
        queryset=Exercise.objects.all(),
        required=False,
        empty_label="Select Exercise",
        label="Exercise",
        widget=forms.Select(attrs={'class': 'exercise-dropdown'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user passed in kwargs
        super().__init__(*args, **kwargs)

        if user:
            # Get exercises that are related to this user's RepMaxes
            exercises_for_user = Exercise.objects.filter(repmax__user=user).distinct()
            self.fields['exercise_names'].queryset = exercises_for_user
