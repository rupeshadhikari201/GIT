from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()

# UserRegistrationTest
class UserRegistrationAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('user_registration')
        
    def test_user_registration_sucess(self):
        
        data = {
            "firstname" :  "Rupesh",
            "lastname"  :   "Aadhikari",
            "email"     : "avecodes@gmail.com",
            "password"  : "123456",
            "cnfpassword" : "123456",
            "user_type"   : "freelancer"
        }
        
        response = self.client.post(self.url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['msg'], "User Registration Sucessfull")
    
    
        def test_user_registration_failure(self):
            data = {
                "username": "",  # Empty username to trigger validation error
                "email": "testuser@example.com",
                "password": "testpassword",
                "user_type": "client"
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginAPITestCase(TestCase):
    
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('user_login')
        self.user = User.objects.create_user(email='testuser@example.com', password='12345', firstname='test', lastname='user', user_type='client')
        self.user.save()

    def test_user_login_success(self):
        data = {
            "email": "testuser@example.com",
            "password": "12345"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['msg'], "User Login Sucessfull")

    def test_user_login_failure(self):
        data = {
            "email": "testuser@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('non_field_errors', response.data['errors'])

    def test_user_login_unverified(self):
        data = {
            "email": "testuser@example.com",
            "password": "12345"
        }
        self.user.is_verified = False
        self.user.save()
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['msg'], "User not verified")