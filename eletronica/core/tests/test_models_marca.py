from django.test import TestCase
from django.db import IntegrityError
from eletronica.core.models import Marca, Modelo


class MarcaModelTest(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(descricao='Marca')

    def test_create(self):
        """Deve criar uma marca"""
        self.assertEqual(1, self.marca.pk)

    def test_str(self):
        """A representação da instância deve retornar a descrição da marca"""
        self.assertEqual('Marca', str(self.marca))


class MarcaUniqueTest(TestCase):
    def setUp(self):
        Marca.objects.create(descricao='Marca')

    def test_unique(self):
        """Descrição deve ser única"""
        marca = Marca(descricao='Marca')
        self.assertRaises(IntegrityError, marca.save)


class ModeloModelTest(TestCase):
    def setUp(self):
        marca = Marca.objects.create(descricao='Marca')
        self.modelo = marca.modelo_set.create(descricao='Modelo')

    def test_create(self):
        """Deve criar um modelo"""
        self.assertEqual(1, self.modelo.pk)

    def test_str(self):
        """A representação da instância deve retornar a marca e o modelo"""
        self.assertEqual('Marca - Modelo', str(self.modelo))


class ModeloUniqueTest(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(descricao='Marca')
        Modelo.objects.create(marca=self.marca, descricao='Modelo')

    def test_unique(self):
        """Modelo + Marca devem ser únicos"""
        modelo = Modelo(marca=self.marca, descricao='Modelo')
        self.assertRaises(IntegrityError, modelo.save)
