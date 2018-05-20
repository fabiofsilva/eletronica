# coding: utf-8
from django.test import TestCase
from django.db import IntegrityError
from eletronica.core.models import Marca, Modelo


class MarcaModelTest(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(descricao=u'Marca')

    def test_create(self):
        """Deve criar uma marca"""
        self.assertEqual(1, self.marca.pk)

    def test_unicode(self):
        """Unicode deve retornar a descrição da marca"""
        self.assertEqual('Marca', unicode(self.marca))


class MarcaUniqueTest(TestCase):
    def setUp(self):
        Marca.objects.create(descricao=u'Marca')

    def test_unique(self):
        """Descrição deve ser única"""
        marca = Marca(descricao=u'Marca')
        self.assertRaises(IntegrityError, marca.save)


class ModeloModelTest(TestCase):
    def setUp(self):
        marca = Marca.objects.create(descricao=u'Marca')
        self.modelo = marca.modelo_set.create(descricao='Modelo')

    def test_create(self):
        """Deve criar um modelo"""
        self.assertEqual(1, self.modelo.pk)

    def test_unicode(self):
        """Unicode deve retornar a marca e o modelo"""
        self.assertEqual(u'Marca - Modelo', unicode(self.modelo))


class ModeloUniqueTest(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(descricao=u'Marca')
        Modelo.objects.create(marca=self.marca, descricao=u'Modelo')

    def test_unique(self):
        """Modelo + Marca devem ser únicos"""
        modelo = Modelo(marca=self.marca, descricao=u'Modelo')
        self.assertRaises(IntegrityError, modelo.save)
