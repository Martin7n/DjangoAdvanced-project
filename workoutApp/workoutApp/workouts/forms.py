from django import forms
from django.forms import modelformset_factory
from .models import Workout, Exercise, WorkoutSet
from ..common_utils.workout_choices import WorkoutType


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['workout_type', 'workout_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['workout_date'].label = 'Select Workout Date'
        self.fields['workout_date'].help_text = 'Default is Today'
        self.fields['workout_date'].widget = forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'placeholder': 'Today',
                'class': 'form-control datepicker',
                'autocomplete': 'off'
            }
        )

        if user:
            self.instance.user = user


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name']

    name = forms.ModelChoiceField(
        queryset=Exercise.objects.all(),
        empty_label="Select Exercise",
        widget=forms.Select(attrs={'class': 'exercise-dropdown'})
    )

    def clean_name(self):
        selected_exercise = self.cleaned_data.get('name')

        if not selected_exercise:
            raise forms.ValidationError('Please select a valid exercise.')
        if selected_exercise not in [x for x in Exercise.objects.all()]:
            raise forms.ValidationError('Please select a valid exercise.')

        return selected_exercise


class WorkoutSetForm(forms.ModelForm):
    class Meta:
        model = WorkoutSet
        fields = ['reps', 'weight', ]

    reps = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Reps'})
                              )

    weight = forms.DecimalField(
        min_value=0,
        required=True,
        decimal_places=2,
        max_digits=5,
        widget=forms.NumberInput(attrs={'placeholder': 'Weight'})
    )


WorkoutSetFormSet = modelformset_factory(
    WorkoutSet,
    form=WorkoutSetForm,
    extra=5,)  # Start with one empty form

ExerciseFormSet = modelformset_factory(
    Exercise,
    form=ExerciseForm,
    extra=5
)


class WorkoutFilterForm(forms.Form):
    WORKOUT_TYPE_CHOICES = WorkoutType.choices

    workout_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(WORKOUT_TYPE_CHOICES),
        required=False,
        label="workout_type",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ExerciseCreateForm(forms.Form):
    class Meta:
        model = Exercise
        fields = ['name', 'category', 'type']

    def clean_name(self):
        new_exercise = self.cleaned_data.get('name')

        if not new_exercise:
            raise forms.ValidationError('Please select a valid exercise.')
        if new_exercise in [x for x in Exercise.objects.all()]:
            raise forms.ValidationError('Please select a valid exercise.')


class ExercisesForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'category', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter exercise name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
