# coding: utf-8
from django.test import TestCase
from django.db import IntegrityError
from eletronica.core.models import Conserto, Defeito, Marca


class ConsertoModelTest(TestCase):
    def setUp(self):
        marca = Marca.objects.create(descricao=u'Marca')
        modelo = marca.modelo_set.create(descricao=u'Modelo')
        defeito = Defeito.objects.create(descricao=u'Defeito')
        self.conserto = Conserto.objects.create(modelo=modelo, defeito=defeito)

    def test_create(self):
        """Deve criar um conserto"""
        self.assertEqual(1, self.conserto.pk)

    def test_unicode(self):
        """Unicode deve retornar o modelo e o defeito"""
        self.assertEqual(u'Modelo - Defeito', unicode(self.conserto))


class ConsertoUniqueTest(TestCase):
    def setUp(self):
        marca = Marca.objects.create(descricao=u'Marca')
        self.modelo = marca.modelo_set.create(descricao=u'Modelo')
        self.defeito = Defeito.objects.create(descricao=u'Defeito')
        Conserto.objects.create(modelo=self.modelo, defeito=self.defeito)

    def test_unique(self):
        """Defeito + Modelo devem ser únicos"""
        conserto = Conserto(modelo=self.modelo, defeito=self.defeito)
        self.assertRaises(IntegrityError, conserto.save)


class SolucaoModelTest(TestCase):
    def setUp(self):
        marca = Marca.objects.create(descricao=u'Marca')
        modelo = marca.modelo_set.create(descricao=u'Modelo')
        defeito = Defeito.objects.create(descricao=u'Defeito')
        conserto = Conserto.objects.create(modelo=modelo, defeito=defeito)
        self.solucao = conserto.solucao_set.create(solucao=u'Solução')

    def test_create(self):
        """Deve criar uma solução"""
        self.assertEqual(1, self.solucao.pk)

    def test_unicode(self):
        """Unicode deve retornar a solução"""
        self.assertEqual(u'Solução', unicode(self.solucao))
