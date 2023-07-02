from rest_framework.test import APITestCase 
from django.urls import reverse 
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User


class AuthenticationTest(APITestCase):
    
    def setUp(self):
        self.username = 'test-user'
        self.password = 'testPassword'
        self.email = 'test@test.test'
        self.bio = 'testbio'
        self.data = {
            "user": {
                'username': self.username,
                'email': self.email,
                'password': self.password   
            }
        }
    
    def test_account_registration_pass(self):
        url = reverse('account-registration')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # response = self.client.post()
    
    def test_account_login_pass(self):
        
        user = User.objects.create_user(
            username=self.username, password=self.password, email=self.email, bio=self.bio
            )
        
        url = reverse('account-login')
        data = {
            'user': {
                'email': self.email,
                'password': self.password
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        


class LoggeInTest(APITestCase):
    
    def setUp(self):
        self.firstUsername = 'testfirstUser'
        self.firstpass = 'firstpass'
        self.firstemail = 'fist@first.first'
        self.secUsername = 'testUsername'
        self.secPass = 'secPass'
        self.secEmail = 'sec@sec.sec'
  