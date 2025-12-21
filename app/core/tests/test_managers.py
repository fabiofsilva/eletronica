from django.test import TestCase
from model_bakery import baker

from core.models import Conserto


class ConsertoManagerTest(TestCase):
    def setUp(self):
        self.samsung = baker.make('core.Marca', descricao='Samsung')
        self.s23 = baker.make('core.Modelo', descricao='S23', marca=self.samsung)

        self.apple = baker.make('core.Marca', descricao='Apple')
        self.iphone = baker.make('core.Modelo', descricao='IPhone', marca=self.apple)

        self.tela_quebrada = baker.make('core.Defeito', descricao='Tela Quebrada')
        self.bateria_inchada = baker.make('core.Defeito', descricao='Bateria Inchada')

        baker.make('core.Conserto', modelo=self.s23, defeito=self.tela_quebrada)
        baker.make('core.Conserto', modelo=self.s23, defeito=self.bateria_inchada)
        baker.make('core.Conserto', modelo=self.iphone, defeito=self.bateria_inchada)

    def test_filtrar_por_marca(self):
        """O Manager deve encontrar Samsung mesmo enviando samsung"""
        qs = Conserto.objects.busca(marca='samsung')
        self.assertEqual(qs.count(), 2)

    def test_filtrar_por_defeito(self):
        """Deve retornar apenas o item com defeito Tela Quebrada."""
        qs = Conserto.objects.busca(defeito=self.tela_quebrada.pk)
        self.assertEqual(qs.count(), 1)

    def test_filtrar_por_modelo(self):
        """Deve encontrar os itens aplicando filtro por modelo"""
        qs = Conserto.objects.busca(modelo=self.s23.descricao)
        self.assertEqual(qs.count(), 2)
