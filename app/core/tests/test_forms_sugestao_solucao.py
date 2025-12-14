from captcha.models import CaptchaStore
from django.test import TestCase

from core.forms import SugestaoSolucaoForm


class SugestaoSolucaoFormTest(TestCase):
    """Testa o formulário de Sugestão de Solução, incluindo a validação do Captcha."""

    def setUp(self):
        # 1. Geração de CAPTCHA Válido para usar nos testes de sucesso
        self.hashkey = CaptchaStore.generate_key()
        # CaptchaStore.objects.get(hashkey=self.hashkey).response contém a resposta correta
        self.captcha_response_correta = CaptchaStore.objects.get(hashkey=self.hashkey).response

        self.valid_data = {
            'email': 'usuario@exemplo.com',
            'sugestao': 'Esta é uma ótima sugestão de solução para o defeito X.',
            # Campos do django-simple-captcha:
            'captcha_0': self.hashkey,  # A chave gerada
            'captcha_1': self.captcha_response_correta,  # A resposta correta
        }

    def test_form_valid_data(self):
        """O formulário deve ser válido com todos os dados (email, sugestão, captcha) corretos."""
        form = SugestaoSolucaoForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), f'O formulário deve ser válido. Erros: {form.errors}')

    def test_captcha_invalido_falha_o_form(self):
        """O formulário deve falhar se a resposta do CAPTCHA estiver incorreta."""
        invalid_captcha_data = self.valid_data.copy()
        invalid_captcha_data['captcha_1'] = 'RESPOSTA_INCORRETA'  # Força a falha

        form = SugestaoSolucaoForm(data=invalid_captcha_data)
        self.assertFalse(form.is_valid())
        self.assertIn('captcha', form.errors)
        self.assertIn('Resposta inválida', form.errors['captcha'][0])

    def test_email_required(self):
        """O campo 'email' é obrigatório."""
        data = self.valid_data.copy()
        data['email'] = ''
        form = SugestaoSolucaoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_sugestao_required(self):
        """O campo 'sugestao' é obrigatório."""
        data = self.valid_data.copy()
        data['sugestao'] = ''
        form = SugestaoSolucaoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('sugestao', form.errors)

    def test_email_format(self):
        """O campo 'email' deve ter um formato de e-mail válido."""
        data = self.valid_data.copy()
        data['email'] = 'email_invalido'
        form = SugestaoSolucaoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
