from django import forms
from .models import Meal
from ..common_utils.workout_choices import MealChoice


class MealCreateForm(forms.ModelForm):
    # We'll define a default value of 3000, as it seems a max realistic amount
    calories = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': 200,
            'max': 3000,
            'step': 200,
            'value': 200,
            'oninput': 'updateCalorieValue(this)',
            'class': 'calorie-slider'
        }),
        label='Calories',
        help_text='Use the slider to select a calorie value between 200 and 3000 in steps of 200.',
    )

    class Meta:
        model = Meal
        fields = ('description', 'calories', 'date', 'type')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['description'].label = 'Default is Today'

    def clean_calories(self):
        calories = self.cleaned_data.get('calories')

        # Ensure calories value is between 200 and 3000 (this should be covered by the widget, but we validate anyway)
        if calories < 200 or calories > 3000:
            raise forms.ValidationError('Calories must be between 200 and 3000.')

        return calories


class MealFilterForm(forms.Form):

    MEAL_TYPE_CHOICES = MealChoice.choices

    meal_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(MEAL_TYPE_CHOICES),
        required=False,
        label="",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class DelMealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ('description', 'calories', 'date', 'type')
