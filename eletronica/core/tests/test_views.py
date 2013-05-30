# coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse as r


class HomePageTest(TestCase):
    def test_get(self):
        'GET deve redirecionar a página (deve retornar 301 porque utilizou a cbv com permanent redirect)'
        resp = self.client.get(r('core:homepage'))
        self.assertEqual(301, resp.status_code)