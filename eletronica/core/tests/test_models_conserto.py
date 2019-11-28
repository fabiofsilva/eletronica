from django.test import TestCase
from django.db import IntegrityError
from eletronica.core.models import Conserto, Defeito, Marca


class ConsertoModelTest(TestCase):
    def setUp(self):
        marca = Marca.objects.create(descricao='Marca')
        modelo = marca.modelo_set.create(descricao='Modelo')
        defeito = Defeito.objects.create(descricao='Defeito')
        self.conserto = Conserto.objects.create(modelo=modelo, defeito=defeito)

    def test_create(self):
        """Deve criar um conserto"""
        self.assertEqual(1, self.conserto.pk)

    def test_str(self):
        """A representação da instância deve retornar a descrição do modelo e do defeito"""
        self.assertEqual('Modelo - Defeito', str(self.conserto))


class ConsertoUniqueTest(TestCase):
    def setUp(self):
        marca = Marca.objects.create(descricao='Marca')
        self.modelo = marca.modelo_set.create(descricao='Modelo')
        self.defeito = Defeito.objects.create(descricao='Defeito')
        Conserto.objects.create(modelo=self.modelo, defeito=self.defeito)

    def test_unique(self):
        """Defeito + Modelo devem ser únicos"""
        conserto = Conserto(modelo=self.modelo, defeito=self.defeito)
        self.assertRaises(IntegrityError, conserto.save)


class SolucaoModelTest(TestCase):
    def setUp(self):
        marca = Marca.objects.create(descricao='Marca')
        modelo = marca.modelo_set.create(descricao='Modelo')
        defeito = Defeito.objects.create(descricao='Defeito')
        conserto = Conserto.objects.create(modelo=modelo, defeito=defeito)
        self.solucao = conserto.solucao_set.create(solucao='Solução')

    def test_create(self):
        """Deve criar uma solução"""
        self.assertEqual(1, self.solucao.pk)

    def test_str(self):
        """A representação da instância deve retornar o texto da solução"""
        self.assertEqual('Solução', str(self.solucao))
