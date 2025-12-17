from unittest.mock import patch

from captcha.models import CaptchaStore
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from core.forms import SugestaoSolucaoForm

HOME_URL = reverse('core:homepage')
SUGESTAO_URL = reverse('core:sugestao_solucao')

# O caminho do patch deve apontar para o local ONDE A FUNÇÃO É USADA (importada)
# e não para o local ONDE A FUNÇÃO É DEFINIDA (core.tasks).
# Isso garante que o mock substitua a referência local no namespace da view.
TASK_PATH = 'core.views.send_proposal_email_async'


class SugestaoSolucaoViewTest(TestCase):
    """Testa a view SugestaoSolucaoView e seu fluxo de trabalho."""

    def setUp(self):
        # Prepara dados válidos, incluindo o captcha
        self.hashkey = CaptchaStore.generate_key()
        self.captcha_response_correta = CaptchaStore.objects.get(hashkey=self.hashkey).response

        self.valid_data = {
            'email': 'testador@exemplo.com',
            'sugestao': 'Esta é a minha sugestão para o problema X.',
            'captcha_0': self.hashkey,
            'captcha_1': self.captcha_response_correta,
        }

    def test_template(self):
        """Requisição GET deve renderizar o template e retornar status 200."""
        response = self.client.get(SUGESTAO_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/sugestao_solucao.html')

    def test_context_has_form(self):
        """Contexto deve ter uma instância de SugestaoSolucaoForm"""
        response = self.client.get(SUGESTAO_URL)
        form = response.context['form']
        self.assertIsInstance(form, SugestaoSolucaoForm)

    @patch(TASK_PATH)  # Mocka a task de envio de e-mail
    def test_post_valid_data_success(self, mock_send_email):
        """POST com dados e CAPTCHA válidos deve chamar a task, redirecionar e mostrar mensagem."""

        response = self.client.post(SUGESTAO_URL, self.valid_data, follow=True)

        # 1. Verifica o status e o redirecionamento (para a home)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, HOME_URL)

        # 2. Verifica se a função de envio assíncrono FOI chamada
        mock_send_email.assert_called_once_with(self.valid_data['email'], self.valid_data['sugestao'])

        mensagem_esperada = 'Obrigado! Os administradores foram notificados sobre a sua sugestão.'
        # 3. Verifica se a mensagem de sucesso foi enviada na resposta
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn(mensagem_esperada, str(messages[0]))

        # 4. Verifica se a mensagem de sucesso foi renderizada no template
        self.assertContains(
            response,
            mensagem_esperada,
            status_code=200,
            msg_prefix='A mensagem de sucesso não foi encontrada no template da página Home.',
        )

    @patch(TASK_PATH)
    def test_post_invalid_captcha(self, mock_send_email):
        """POST com CAPTCHA inválido deve re-renderizar o formulário e não enviar e-mail."""

        invalid_captcha_data = self.valid_data.copy()
        invalid_captcha_data['captcha_1'] = 'RESPOSTA_ERRADA'

        response = self.client.post(SUGESTAO_URL, invalid_captcha_data)

        # 1. Não deve redirecionar (status 200)
        self.assertEqual(response.status_code, 200)

        # 2. Verifica se o e-mail NÃO foi enviado
        mock_send_email.assert_not_called()

        # 3. Verifica se o erro do captcha está no contexto
        self.assertIn('Resposta inválida', response.content.decode())

    @patch(TASK_PATH)
    def test_post_invalid_form_data(self, mock_send_email):
        """POST com dados de formulário inválidos (ex: email vazio) deve re-renderizar e não enviar e-mail."""

        invalid_data = self.valid_data.copy()
        invalid_data['email'] = ''  # Email vazio (inválido)

        response = self.client.post(SUGESTAO_URL, invalid_data)

        # 1. Não deve redirecionar (status 200)
        self.assertEqual(response.status_code, 200)

        # 2. Verifica se o e-mail NÃO foi enviado
        mock_send_email.assert_not_called()

        # 3. Verifica se o erro do campo está presente
        self.assertIn('Este campo é obrigatório.', response.content.decode())

    def test_sugestao_solucao_is_noindex(self):
        """Contexto deve ter seo no index (noxindex=True)"""
        response = self.client.get(SUGESTAO_URL)
        self.assertTrue(response.context['noindex'])
