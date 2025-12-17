from django.test import TestCase


class RobotsTest(TestCase):
    """
    Testes do endpoint /robots.txt.

    Este endpoint é tratado como um recurso técnico:
    - Não é HTML
    - Não usa base.html
    - Pode estar cacheado
    - Não deve depender de template rendering

    Por isso, os testes validam apenas:
    - Disponibilidade do endpoint
    - Tipo de conteúdo retornado
    - Conteúdo textual esperado
    """

    def setUp(self):
        self.resp = self.client.get('/robots.txt')

    def test_get(self):
        """GET deve retornar status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_robots_txt_content(self):
        """
        Valida o conteúdo do robots.txt.

        Verificações:
        - Content-Type deve ser text/plain
        - Deve permitir acesso a todos os agentes (*)
        - Deve permitir crawl do site inteiro (/)

        Não testamos template, cache ou formatação,
        apenas o contrato mínimo esperado por crawlers.
        """
        self.assertEqual(self.resp['Content-Type'], 'text/plain')
        self.assertContains(self.resp, 'User-agent: *')
        self.assertContains(self.resp, 'Allow: /')
