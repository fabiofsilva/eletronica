from django.test import TestCase
from django.urls import reverse


class SeoContextProcessorTest(TestCase):
    """
    Testes do context processor de SEO.
    Este teste garante o CONTRATO mínimo de SEO da aplicação:
    - As variáveis básicas sempre existem no contexto
    - Valores padrão são seguros
    - SEO não depende da boa vontade de cada view
    """

    def test_seo_defaults_are_available(self):
        # Faz uma requisição simples para qualquer view pública
        response = self.client.get(reverse('core:homepage'))
        # Verifica se as variáveis de SEO existem no contexto
        self.assertIn('seo_title', response.context)
        self.assertIn('seo_description', response.context)
        self.assertIn('seo_image', response.context)
        self.assertIn('noindex', response.context)
        # Confirma que o site é indexável por padrão
        self.assertFalse(response.context['noindex'])
        # Garante que a imagem de SEO não é vazia
        # (não testamos o arquivo físico, apenas a existência do valor)
        self.assertTrue(response.context['seo_image'])
