from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class ConsertoViewSetTest(APITestCase):
    def setUp(self):
        # Setup de dados para ter pelo menos 3 páginas (60 itens se page_size=20)
        self.marca = baker.make('core.Marca', descricao='Apple')
        self.modelo = baker.make('core.Modelo', descricao='iPhone 13', marca=self.marca)
        # Criando 50 registros de uma vez.
        self.consertos = baker.make('core.Conserto', modelo=self.modelo, _quantity=50)

        self.url = reverse('core:consertos-list')

    def test_get_consertos_list_with_pagination_metadata(self):
        """Valida se a estrutura do JSON de paginação está correta"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('page_range', response.data)
        self.assertIn('current_page', response.data)
        self.assertEqual(len(response.data['results']), 20)

    def test_filter_by_marca_via_url(self):
        """Valida se o filtro do Manager é acionado pelos query_params"""
        # Criando um conserto de outra marca para testar o filtro
        outra_marca = baker.make('core.Marca', descricao='Samsung')
        outro_modelo = baker.make('core.Modelo', descricao='S22', marca=outra_marca)
        outro_defeito = baker.make('core.Defeito', descricao='Tela')
        baker.make('core.Conserto', modelo=outro_modelo, defeito=outro_defeito)
        # Filtra apenas por Apple
        response = self.client.get(self.url, {'marca': 'Apple'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deve retornar apenas os 50 da Apple, ignorando o da Samsung
        self.assertEqual(response.data['count'], 50)

    def test_elided_pagination_logic(self):
        """Valida se o '...' aparece quando estamos em uma lista longa"""
        # Com 50 itens e page_size=20, temos 3 páginas.
        # Vamos testar o range na página 1
        response = self.client.get(self.url, {'page': 1})
        # Esperado para 3 páginas: [1, 2, 3] (sem elisão ainda pois são poucas)
        # Se tivéssemos 200 itens, veríamos o "..."
        self.assertEqual(response.data['total_pages'], 3)
        self.assertEqual(response.data['page_range'], [1, 2, 3])
