from django.test import TestCase
from django.test import TestCase, SimpleTestCase
from django.shortcuts import reverse
from .models import User

# Create your tests here.


class HomePageTests(SimpleTestCase):

    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_index_url_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')