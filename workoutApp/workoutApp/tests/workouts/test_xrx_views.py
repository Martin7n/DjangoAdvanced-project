from django.urls import reverse
from django.test import TestCase
from workoutApp.users.models import CustomUser


class ExerciseCreateViewTest(TestCase):

    def setUp(self):

        self.staff_user = CustomUser.objects.create_user(
            username='staff',
            password='@@12345',
            is_staff=True,
            email="tst@tst.com")
        self.normal_user = CustomUser.objects.create_user(
            username='user',
            password='@@12345',
            email="estst@tst.com")
        self.url = reverse('exercise-list')
        self.url2 = reverse('exercise-create')

    def test_access_for_staff_user_exercise_list_view(self):

        self.client.login(username='staffuser', password='@@12345')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workouts/exercise_list.html')

    def test_access_for_non_staff_user_exercise_list_view(self):
        self.client.login(username='user', password='@@12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workouts/exercise_list.html')

    def test_access_for_non_staff_user(self):

        self.client.login(username='user', password='@@12345')
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 403)
        self.assertIn(b"You do not have permission to that function", response.content)
