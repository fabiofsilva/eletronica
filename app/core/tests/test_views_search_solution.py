from django.core.paginator import Page
from django.test import TestCase
from django.urls import reverse as r
from model_bakery import baker


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
        # Leva em consideração o input csrfmiddlewaretoken
        self.assertContains(self.resp, '<input', 3)
        self.assertContains(self.resp, '<div id="results"')
        self.assertContains(self.resp, 'type="text"', 2)
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """HTML deve conter csrf token"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_context(self):
        """Contexto deve ter uma lista de defeitos"""
        self.assertIn('defeitos', self.resp.context)


class SearchRepairListTest(TestCase):
    def setUp(self):
        conserto = baker.make('core.Conserto', 30)
        self.conserto_pk = conserto[0].pk
        self.resp = self.client.post(r('core:conserto_list'))

    def test_post(self):
        """GET deve retornar status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Template deve ser core/conserto_list.html"""
        self.assertTemplateUsed(self.resp, 'core/conserto_list.html')

    def test_html(self):
        """HTML deve conter uma lista de consertos e paginação"""
        self.assertContains(self.resp, '<ul class="list-unstyled space-y-3"')
        self.assertContains(self.resp, f'href="/consertos/{self.conserto_pk}/">Defeito: ')
        self.assertContains(self.resp, '<nav aria-label="Navegação de Resultados"')
        # Teste da renderização dos botões anterior e próximo
        self.assertContains(self.resp, '<span aria-hidden="true">', 2)
        # Teste da renderização dos botões de paginação
        self.assertContains(
            self.resp,
            '<li class="page-item active"><a href="#" class="page-link pagination-link" data-page="1">1</a></li>',
        )
        self.assertContains(
            self.resp,
            '<li class="page-item"><a href="#" class="page-link pagination-link" data-page="2">2</a></li>'
        )

    def test_context(self):
        """Contexto deve conter uma instância de Page"""
        p = self.resp.context['consertos']
        self.assertIsInstance(p, Page)


class SearchRepairListFilterTest(TestCase):
    def setUp(self):
        # 1. Cria o primeiro conserto (esperado como resultado dos filtros)
        nao_liga = baker.make('core.Defeito', descricao='NÃO LIGA')
        modelo_cce = baker.make('core.Modelo', marca__descricao='CCE', descricao='HPS-2071')
        baker.make('core.Conserto', modelo=modelo_cce, defeito=nao_liga)
        # 2. Cria o segundo conserto (esperado ser excluído pelos filtros)
        fonte_alta = baker.make('core.Defeito', descricao='FONTE ALTA')
        modelo_philco = baker.make('core.Modelo', marca__descricao='PHILCO', descricao='PC-1416')
        baker.make('core.Conserto', modelo=modelo_philco, defeito=fonte_alta)
        # Armazena o PK do primeiro defeito para uso no teste de filtro
        self.defeito_pk = nao_liga.pk

    def test_post_marca(self):
        """Deve filtrar e retornar apenas o conserto da marca 'CCE'."""
        self.result_expected({'marca': 'CCE'})

    def test_post_modelo(self):
        """Deve filtrar e retornar apenas o conserto do modelo 'HPS-2071'."""
        self.result_expected({'modelo': 'HPS-2071'})

    def test_post_defeito(self):
        """Deve filtrar e retornar apenas o conserto com o defeito 'NÃO LIGA' (usando o PK)."""
        self.result_expected({'defeito': self.defeito_pk})

    def result_expected(self, data):
        """Verifica se a resposta contém o conserto CCE/HPS-2071 e exclui o conserto PHILCO/PC-1416."""
        resp = self.client.post(r('core:conserto_list'), data)
        self.assertContains(resp, 'NÃO LIGA</a>')
        self.assertContains(resp, '<p class="small text-muted mb-0">Modelo: HPS-2071 | Marca: CCE</p>')
        self.assertNotContains(resp, 'FONTE ALTA</a>')
        self.assertNotContains(resp, '<p class="small text-muted mb-0">Modelo: PC-1416 | Marca: PHILCO</p>')
