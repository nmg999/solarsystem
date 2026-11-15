from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse


class AccountTests(TestCase):
    password = 'A-test-only-passphrase!7492'

    def test_signup_logs_in_and_hashes_password(self):
        response = self.client.post(reverse('learning:signup'), {
            'username': 'newlearner',
            'password1': self.password,
            'password2': self.password,
        })
        self.assertRedirects(response, reverse('learning:home'))
        user = get_user_model().objects.get(username='newlearner')
        self.assertNotEqual(user.password, self.password)
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertContains(self.client.get('/'), 'Hi, newlearner')

    def test_invalid_signup_does_not_create_user(self):
        response = self.client.post(reverse('learning:signup'), {
            'username': 'newlearner',
            'password1': self.password,
            'password2': 'different-password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(get_user_model().objects.exists())

    def test_login_and_logout(self):
        get_user_model().objects.create_user('learner', password=self.password)
        response = self.client.post(reverse('learning:login'), {
            'username': 'learner', 'password': 'incorrect',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        response = self.client.post(reverse('learning:login'), {
            'username': 'learner', 'password': self.password,
            'next': 'https://example.org/untrusted',
        })
        self.assertRedirects(response, reverse('learning:home'))
        self.assertEqual(self.client.get(reverse('learning:logout')).status_code, 405)
        response = self.client.post(reverse('learning:logout'))
        self.assertRedirects(response, reverse('learning:home'))
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertContains(self.client.get('/'), 'Sign up')

    def test_signup_requires_csrf_token(self):
        response = Client(enforce_csrf_checks=True).post(reverse('learning:signup'), {
            'username': 'learner', 'password1': self.password, 'password2': self.password,
        })
        self.assertEqual(response.status_code, 403)
