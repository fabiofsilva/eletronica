from unittest.mock import patch

from django.core import mail
from django.test import TestCase

from core.tasks import send_proposal_email_async


class SendProposalEmailAsyncTest(TestCase):
    """Testa a função de envio de e-mail assíncrono e a gravação de log."""

    def setUp(self):
        # Limpa a caixa de saída de e-mails do Django antes de cada teste
        mail.outbox = []
        # Dados padrão para o teste
        self.email = 'usuario_task@teste.com'
        self.sugestao = 'Este é o conteúdo da sugestão de teste.'

    @patch('django.core.mail.EmailMessage.send')
    def test_email_sent_successfully(self, mock_email_send):
        """O e-mail deve ser construído e tentado o envio corretamente."""

        with self.settings(ADMINS=[('Admin 1', 'admin1@site.com')]):
            send_proposal_email_async(self.email, self.sugestao)

        # 1. Verifica se a função de envio foi chamada
        mock_email_send.assert_called_once()

    @patch('logging.Logger.error')  # Mocka a chamada do logger
    @patch('django.core.mail.EmailMessage.send')  # Mocka o envio de e-mail
    def test_email_send_error_logs_to_disk(self, mock_email_send, mock_log_error):
        """Em caso de erro no envio do e-mail, deve gravar um log usando o logger 'proposal'."""

        # Simula um erro que ocorreria durante o envio real (Ex: erro de conexão)
        mock_email_send.side_effect = Exception("Erro de conexão simulado SMTP")

        with self.settings(ADMINS=[('Admin Teste', 'admin_teste@site.com')]):
            send_proposal_email_async(self.email, self.sugestao)

        # 1. Verifica se o logger 'proposal' foi chamado para gravar o erro
        mock_log_error.assert_called_once()

        # 2. Verifica se a mensagem de log contém as informações essenciais
        log_message = mock_log_error.call_args[0][0]
        self.assertIn('Falha ao enviar e-mail de sugestão.', log_message)
        self.assertIn(self.email, log_message)
        self.assertIn(self.sugestao, log_message)
