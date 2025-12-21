from django.core.paginator import Paginator
from django.test import RequestFactory, TestCase

from core.pagination import ElidedPagination


class ElidedPaginationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.pagination = ElidedPagination()
        # Criamos um dataset grande (200 itens) para garantir que a
        # lógica de elisão (os '...') seja acionada pelo Paginator.
        self.queryset = list(range(1, 201))

    def test_pagination_returns_elided_range_at_first_page(self):
        """
        Testa se o JSON de resposta contém o range inteligente [1, 2, '...', 10]
        quando estamos na primeira página.
        """
        # 1. SIMULAÇÃO DE REQUEST:
        # Criamos um request fake. O DRF precisa disso para construir URLs
        # (como 'next' e 'previous'), mesmo que aqui foquemos no range.
        request = self.factory.get('/', {'page': 1})
        # 2. SIMULAÇÃO DO FLUXO DO DJANGO:
        # O DRF usa o Paginator nativo do Django para fatiar o QuerySet.
        # Com 200 itens e page_size 20, teremos 10 páginas.
        paginator = Paginator(self.queryset, 20)
        page = paginator.page(1)
        paginator_ellipsis = paginator.ELLIPSIS
        # 3. "DENTRO DA CAIXA PRETA" DO DRF:
        # Em uma execução normal, o DRF faz as duas linhas abaixo internamente.
        # Aqui, estamos 'injetando' manualmente o que a classe espera:
        self.pagination.request = request  # Necessário para os métodos get_next_link/get_previous_link
        self.pagination.page = page  # A página atual com os 20 objetos e metadados
        # 4. EXECUÇÃO DA FORMATAÇÃO DO JSON:
        # Chamamos o a função customizada.
        response = self.pagination.get_paginated_response(page.object_list)
        # 5. VALIDAÇÃO DO CONTRATO COM O FRONT-END:
        data = response.data
        # Verificamos se a estrutura de dados que o Front vai consumir está correta
        self.assertIn('page_range', data)
        self.assertIn(paginator_ellipsis, data['page_range'])
        # Na página 1, com on_each_side=1 e on_ends=1, o esperado é:
        # [1, 2, "...", 10]
        expected_range = [1, 2, paginator_ellipsis, 10]
        self.assertEqual(data['page_range'], expected_range)
        self.assertEqual(data['total_pages'], 10)
        self.assertEqual(data['current_page'], 1)

    def test_pagination_range_middle_page(self):
        """
        Testa a janela deslizante quando o usuário está no meio da lista.
        Ex: Na página 5 de 10, deve mostrar [1, '...', 4, 5, 6, '...', 10]
        """
        # 1. Preparamos o ambiente (Página 5 de 10)
        paginator = Paginator(self.queryset, 20)
        page = paginator.page(5)
        paginator_ellipsis = paginator.ELLIPSIS
        # 2. Criamos o request para que o DRF possa gerar os links de 'next' e 'prev'
        request = self.factory.get('/', {'page': 5})
        # 3. ATRIBUIÇÃO COMPLETA: Injetamos o estado que o DRF injetaria
        self.pagination.request = request  # <--- O ponto que faltava
        self.pagination.page = page
        # 4. Executamos a formatação do JSON
        response = self.pagination.get_paginated_response(page.object_list)
        # 5. Validação da lógica de "janela" (on_each_side=1, on_ends=1)
        expected_range = [1, paginator_ellipsis, 4, 5, 6, paginator_ellipsis, 10]
        self.assertEqual(response.data['page_range'], expected_range)
        self.assertTrue(response.data['has_next'])
        self.assertTrue(response.data['has_prev'])
