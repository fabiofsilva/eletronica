from django.test import TestCase
from django.db import IntegrityError
from eletronica.core.models import Defeito


class DefeitoModelTest(TestCase):
    def setUp(self):
        self.defeito = Defeito.objects.create(descricao='Defeito')

    def test_create(self):
        """Deve criar um tipo defeito"""
        self.assertEqual(1, self.defeito.pk)

    def test_str(self):
        """A representação da instância deve retornar a descrição"""
        self.assertEqual('Defeito', str(self.defeito))


class DefeitoUniqueTest(TestCase):
    def setUp(self):
        Defeito.objects.create(descricao='Defeito')

    def test_unique(self):
        """Descrição do defeito deve ser única"""
        defeito = Defeito(descricao='Defeito')
        self.assertRaises(IntegrityError, defeito.save)
