# tests/accounts/test_views.py

from django.test import TestCase
from django.urls import reverse

from workoutApp.accounts.models import CustomUser


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='@12345', email="tst@tst.com")
        self.client.login(username='testuser', password='@12345', email="estst@tst.com")

    def test_view_profile_logged_user_own_profile(self):
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, 200)

    def test_view_profile_non_logged_user(self):
        self.client.logout()
        response = self.client.get(reverse('user-profile'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("user-profile")}')


class DeleteProfileViewTest(TestCase):
    def setUp(self):
        self.staff_user = CustomUser.objects.create_user(username='staff', password='@@12345', is_staff=True,email="tst@tst.com")
        self.normal_user = CustomUser.objects.create_user(username='user', password='@@12345', email="estst@tst.com")

    def test_delete_profile_by_auth_staff_user(self):
        self.client.login(username='staff', password='@@12345')
        response = self.client.get(reverse('delete-profile', args=[self.normal_user.pk]))
        self.assertRedirects(response, reverse('all-profiles'))
        self.assertEqual(CustomUser.objects.filter(username='user').count(), 0)

    def test_delete_staff_by_non_staff_user(self):
        self.client.login(username='user', password='@@12345')
        response = self.client.get(reverse('delete-profile', args=[self.staff_user.pk]))
        self.assertEqual(CustomUser.objects.filter(username='user').count(), 1)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("delete-profile", args=[self.staff_user.pk])}')

