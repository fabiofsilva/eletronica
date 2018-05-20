# coding: utf-8
from django.test import TestCase
from django.db import IntegrityError
from eletronica.core.models import Defeito


class DefeitoModelTest(TestCase):
    def setUp(self):
        self.defeito = Defeito.objects.create(descricao=u'Defeito')

    def test_create(self):
        """Deve criar um tipo defeito"""
        self.assertEqual(1, self.defeito.pk)

    def test_unicode(self):
        """Unicode deve retornar a descrição"""
        self.assertEqual(u'Defeito', unicode(self.defeito))


class DefeitoUniqueTest(TestCase):
    def setUp(self):
        Defeito.objects.create(descricao=u'Defeito')

    def test_unique(self):
        """Descrição do defeito deve ser única"""
        defeito = Defeito(descricao=u'Defeito')
        self.assertRaises(IntegrityError, defeito.save)
