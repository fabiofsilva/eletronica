from django.test import TestCase
from django.urls import reverse as r
from model_mommy import mommy
from eletronica.core.models import Conserto


class ConsertoDetailTest(TestCase):
    def setUp(self):
        modelo = mommy.make('core.Modelo', marca__descricao='CCE', descricao='HPS-2071')
        conserto = mommy.make('core.Conserto', modelo=modelo, defeito__descricao='NÃO LIGA')
        mommy.make('core.Solucao', conserto=conserto, solucao='Ver capacitor C1', _quantity=2)
        conserto.solucao_set.create()
        self.resp = self.client.get(r('core:conserto_detail', kwargs={'pk': conserto.pk}))

    def test_get(self):
        """GET deve retornar status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Template deve ser core/conserto_detail.html"""
        self.assertTemplateUsed(self.resp, 'core/conserto_detail.html')

    def test_conserto_context(self):
        """Contexto deve ter uma instância de Conserto"""
        conserto = self.resp.context['conserto']
        self.assertIsInstance(conserto, Conserto)

    def test_html(self):
        """Html deve conter informações do conserto e soluções"""
        self.assertContains(self.resp, 'CCE - HPS-2071 - NÃO LIGA')
        self.assertContains(self.resp, 'Ver capacitor C1', 2)
