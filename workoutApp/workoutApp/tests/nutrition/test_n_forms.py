from django.test import TestCase
from datetime import date

from workoutApp.nutrition.forms import MealCreateForm
from workoutApp.accounts.models import CustomUser


class MealCreateFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testouser', password='@@12345')
        self.client.login(username='testouser', password='@@12345')

    def test_valid_form(self):
        data = {
            'description': 'Testo Meal',
            'calories': 500,
            'date': date.today(),
            'type': 'Lunch',
        }
        form = MealCreateForm(data=data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_calories(self):
        data = {
            'description': 'Testo Meal',
            'calories': 3500,
            'date': date.today(),
            'type': 'Dinner',
        }
        form = MealCreateForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('Calories must be between 200 and 3000.', form.errors['calories'])


