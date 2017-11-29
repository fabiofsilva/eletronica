# coding: utf-8
from django.test import TestCase
from django.urls import reverse as r


class HomePageTest(TestCase):
    def test_get(self):
        'GET deve redirecionar a página para o login do admin'
        resp = self.client.get(r('core:homepage'), follow=True)
        self.assertRedirects(resp, '/admin/login/?next=/admin/')