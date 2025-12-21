from django.test import TestCase
from django.urls import reverse as r


class SearchRepairTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:search_repair'))

    def test_get(self):
        """GET deve retornar status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Template deve ser core/search_repair.html"""
        self.assertTemplateUsed(self.resp, 'core/search_repair.html')

    def test_html(self):
        """HTML deve conter inputs"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<select')
        self.assertContains(self.resp, '<input', 2)
        self.assertContains(self.resp, '<div id="results"')
        self.assertContains(self.resp, 'type="text"', 2)
        self.assertContains(self.resp, 'type="submit"')

    def test_context(self):
        """Contexto deve ter uma lista de defeitos"""
        self.assertIn('defeitos', self.resp.context)
