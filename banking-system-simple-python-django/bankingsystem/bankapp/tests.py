from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from bankapp.models import UserProfile

class UserAuthenticationTests(TestCase):

    def test_user_signup(self):
        """Test if a new user can successfully sign up."""
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Check if redirected after signup
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Check if user is created
        self.assertTrue(UserProfile.objects.filter(user__username='testuser').exists())  # Check if profile is created

    def test_duplicate_user_signup(self):
        """Test if trying to sign up with an existing username fails."""
        User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'newemail@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)  # Should not redirect on failure
        self.assertContains(response, 'A user with that username already exists.')

    def test_login(self):
        """Test if a registered user can log in successfully."""
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Check if redirected after login
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)  # Check if user is authenticated

    def test_logout(self):
        """Test if a logged-in user can log out."""
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Check if redirected after logout
        self.assertNotIn('_auth_user_id', self.client.session)  # Check if user is logged out
