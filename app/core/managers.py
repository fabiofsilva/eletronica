from django.db import models


class ConsertoQuerySet(models.QuerySet):
    def busca(self, marca=None, modelo=None, defeito=None):
        """
        Filtra o conjunto de consertos com base nos critérios de marca, modelo e defeito.

        A busca por marca e modelo é realizada utilizando o lookup '__icontains',
        enquanto a busca por defeito utiliza a chave primária exata.

        :param marca: Nome ou parte do nome da marca do fabricante (via modelo__marca).
        :type marca: str, optional

        :param modelo: Descrição ou parte da descrição do modelo do dispositivo.
        :type modelo: str, optional

        :param defeito: Identificador único (PK) do tipo de defeito relatado.
        :type defeito: int, optional

        :return: Um QuerySet filtrado com os parâmetros fornecidos.
        :rtype: django.db.models.query.QuerySet
        """
        filters = {}

        if marca:
            filters['modelo__marca__descricao__icontains'] = marca

        if modelo:
            filters['modelo__descricao__icontains'] = modelo

        if defeito:
            filters['defeito__pk'] = defeito

        return self.filter(**filters)
