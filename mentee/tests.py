from django.test import TestCase
from django.test import TestCase, SimpleTestCase
from django.shortcuts import reverse
from .models import User

# Create your tests here.


class HomePageTests(SimpleTestCase):

    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)