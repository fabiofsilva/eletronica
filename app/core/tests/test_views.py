from django.test import TestCase
from django.urls import reverse as r


class HomePageTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:homepage'))

    def test_get(self):
        """GET deve retornar status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Template deve ser homepage.html"""
        self.assertTemplateUsed(self.resp, 'core/homepage.html')
