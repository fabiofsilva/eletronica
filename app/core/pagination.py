from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ElidedPagination(PageNumberPagination):
    """
    Classe de paginação customizada para o Django REST Framework que fornece
    metadados detalhados para navegação inteligente (estilo Google/Amazon).

    O diferencial desta classe é o campo `page_range`, que utiliza a lógica
    de elisão do Django para retornar uma lista de números de página intercalada
    com reticências ("..."), permitindo que o front-end renderize uma régua de
    navegação compacta.

    A estrutura do JSON de resposta inclui:
    - count: Total de itens no banco de dados.
    - total_pages: Total de páginas calculadas.
    - current_page: Índice da página atual.
    - has_next / has_prev: Booleanos para controle de visibilidade de setas.
    - page_range: Lista misturando ints e str (Ex: [1, 2, "...", 7, 8]).
    - results: Os dados serializados da página atual.
    """

    def get_paginated_response(self, data):
        """
        Sobrescreve a resposta padrão para injetar o range de páginas elidido.

        :param data: Lista de dados já serializados pelo Serializer da View.
        :return: Objeto Response do DRF com metadados de paginação e resultados.
        """
        paginator = self.page.paginator
        current_page = self.page.number

        # A função get_elided_page_range gera a lógica de "janela deslizante".
        # on_each_side: define quantos números aparecem colados à página atual.
        # on_ends: define quantos números aparecem nas extremidades (início e fim).
        elided_range = paginator.get_elided_page_range(
            current_page,
            on_each_side=1,
            on_ends=1,
        )

        return Response(
            {
                'count': paginator.count,
                'total_pages': paginator.num_pages,
                'current_page': current_page,
                'has_next': self.get_next_link() is not None,
                'has_prev': self.get_previous_link() is not None,
                'page_range': list(elided_range),  # Transforma o gerador em lista para o JSON
                'results': data,
            }
        )
