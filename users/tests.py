from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        print(response.content)  # Print page return content
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_login(self):
        User.objects.create_user(username='testuser',email='testuser@example.com', password='testpass123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_password_change(self):
        user = User.objects.create_user(username='testuser',email='testuser@example.com', password='oldpassword123')
        self.client.login(username='testuser', password='oldpassword123')

        response = self.client.post(reverse('change_password'), {
            'old_password': 'oldpassword123',
            'new_password1': 'newcomplexpass123',
            'new_password2': 'newcomplexpass123',
        })

        user.refresh_from_db()

        # The password was successfully changed. Procedure
        self.assertTrue(user.check_password('newcomplexpass123'))

        # Modify the test code to match what the Django view returns
        self.assertJSONEqual(response.content, {"message": "Password changed successfully"})
