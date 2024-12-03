# tests/accounts/test_models.py

from django.test import TestCase

from workoutApp.accounts.models import CustomUser, UserProfile


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

    def test_created_user_profile(self):
        profile = self.user.profile
        self.assertEqual(profile.user, self.user)

    def test_profile_is_public(self):
        profile = self.user.profile
        self.assertFalse(profile.is_public)

    def test_default_profile_picture(self):
        profile = self.user.profile
        self.assertEqual(profile.profile_picture.name, 'default_profile.jpg')




