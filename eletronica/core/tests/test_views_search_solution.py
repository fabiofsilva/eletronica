# coding: utf-8
from django.test import TestCase
from django.urls import reverse as r
from django.core.paginator import Page
from model_mommy import mommy


class SearchRepairTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('core:search_repair'))
        
    def test_get(self):
        'GET deve retornar status code 200'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'Template deve ser core/search_repair.html'
        self.assertTemplateUsed(self.resp, 'core/search_repair.html')
        
    def test_html(self):
        'HTML deve conter inputs'
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<select')        
        self.assertContains(self.resp, '<input', 4)
        self.assertContains(self.resp, '<div id="results"')
        self.assertContains(self.resp, 'type="text"', 2)
        self.assertContains(self.resp, 'type="button"')
        
    def test_csrf(self):
        'HTML deve conter csrf token'
        self.assertContains(self.resp, 'csrfmiddlewaretoken')
        
    def test_context(self):
        'Contexto deve ter uma lista de defeitos'
        self.assertIn('defeitos', self.resp.context)
        
        
class SearchRepairListTest(TestCase):
    def setUp(self):
        mommy.make('core.Conserto', 30)
        self.resp = self.client.post(r('core:conserto_list'))
        
    def test_post(self):
        'GET deve retornar status code 200'
        self.assertEqual(200, self.resp.status_code)
        
    def test_template(self):
        'Template deve ser core/conserto_list.html'
        self.assertTemplateUsed(self.resp, 'core/conserto_list.html')
        
    def test_html(self):
        'HTML deve conter uma tabela com lista de consertos'
        self.assertContains(self.resp, '<table')
        self.assertContains(self.resp, '<a href="/consertos/1/">')
        self.assertContains(self.resp, '<div class="pagination pagination-centered"')
        self.assertContains(self.resp, '<li class="disabled"><span>1</span></li>')
        self.assertContains(self.resp, '<li><a href="#" onclick="repair_search(2)" class="previous">2</a></li>')
        self.assertContains(self.resp, '<a href="#" onclick="repair_search(2)" class="next">Next</a>')
                
    def test_context(self):
        'Contexto deve conter uma instância de Page'
        p = self.resp.context['consertos']
        self.assertIsInstance(p, Page)
        
class SearchRepairListFilterTest(TestCase):
    def setUp(self):
        modelo = mommy.make('core.Modelo', marca__descricao=u'CCE', descricao='HPS-2071')
        mommy.make('core.Conserto', modelo=modelo, defeito__descricao=u'NÃO LIGA')
        modelo = mommy.make('core.Modelo', marca__descricao=u'PHILCO', descricao='PC-1416')
        mommy.make('core.Conserto', modelo=modelo, defeito__descricao=u'FONTE ALTA')
        
    def test_post_marca(self):
        'Teste com filtro por marca'
        self.result_expected({'marca': u'CCE'})
        
    def test_post_modelo(self):
        'Teste com filtro por modelo'
        self.result_expected({'modelo': u'HPS-2071'})

    def test_post_defeito(self):
        'Teste com filtro por defeito'
        self.result_expected({'defeito': u'1'})
                
    def result_expected(self, data):
        resp = self.client.post(r('core:conserto_list'), data)
        self.assertContains(resp, '<td>CCE</td>')
        self.assertContains(resp, '<td>HPS-2071</td>')
        self.assertContains(resp, '<td>NÃO LIGA</td>')
        self.assertNotContains(resp, '<td>PHILCO</td>')
        self.assertNotContains(resp, '<td>PC-1416</td>')
        self.assertNotContains(resp, '<td>FONTE ALTA</td>')