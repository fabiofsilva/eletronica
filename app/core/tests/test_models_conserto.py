from django.db import IntegrityError
from django.test import TestCase
from django.utils.text import slugify

from core.models import Conserto, Defeito, Marca


class ConsertoModelTest(TestCase):
    def setUp(self):
        marca = Marca.objects.create(descricao='Marca')
        modelo = marca.modelo_set.create(descricao='Modelo')
        defeito = Defeito.objects.create(descricao='Defeito')
        self.conserto = Conserto.objects.create(modelo=modelo, defeito=defeito, diagnostico='Diagnóstico')

    def test_create(self):
        """Deve criar um conserto"""
        self.assertEqual(1, self.conserto.pk)

    def test_str(self):
        """A representação da instância deve retornar a descrição do modelo e do defeito"""
        self.assertEqual('Modelo - Defeito', str(self.conserto))

    def test_slug(self):
        """O slug deve ser composto pela descrição do modelo e descrição do defeito"""
        slug = slugify('Modelo-Defeito')
        self.assertEqual(slug, self.conserto.slug)

    def test_get_absolute_url(self):
        """
        Garante que a função get_absolute_url() retorna a URL canônica
        baseada em slug, e não em PK ou outro identificador interno.
        """
        self.assertEqual(f'/consertos/{self.conserto.slug}/', self.conserto.get_absolute_url())


class ConsertoUniqueTest(TestCase):
    def setUp(self):
        marca = Marca.objects.create(descricao='Marca')
        self.modelo = marca.modelo_set.create(descricao='Modelo')
        self.defeito = Defeito.objects.create(descricao='Defeito')
        Conserto.objects.create(modelo=self.modelo, defeito=self.defeito, diagnostico='Diagnóstico')

    def test_unique(self):
        """Defeito + Modelo devem ser únicos"""
        conserto = Conserto(modelo=self.modelo, defeito=self.defeito, diagnostico='Diagnóstico')
        self.assertRaises(IntegrityError, conserto.save)


class SolucaoModelTest(TestCase):
    def setUp(self):
        marca = Marca.objects.create(descricao='Marca')
        modelo = marca.modelo_set.create(descricao='Modelo')
        defeito = Defeito.objects.create(descricao='Defeito')
        conserto = Conserto.objects.create(modelo=modelo, defeito=defeito, diagnostico='Diagnóstico')
        self.solucao = conserto.solucao_set.create(solucao='Solução')

    def test_create(self):
        """Deve criar uma solução"""
        self.assertEqual(1, self.solucao.pk)

    def test_str(self):
        """A representação da instância deve retornar o texto da solução"""
        self.assertEqual('Solução', str(self.solucao))
