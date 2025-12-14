import logging
import threading

from django.conf import settings
from django.core.mail import EmailMessage

# Obtém o logger configurado no settings
logger = logging.getLogger('proposal')


def _send_email_in_thread(from_email, proposal):
    """
    Função privada que executa o envio do e-mail.
    :param from_email: e-mail do usuário que sugeriu uma solução.
    :param proposal: Solução proposta pelo usuário.
    """
    try:
        # 1. Preparação do E-mail
        subject = '[Sugestão] Nova Sugestão de Solução Recebida'

        body = (
            f'Uma nova sugestão de solução foi enviada por um usuário público.\n\n'
            f'E-mail do remetente: {from_email}\n'
            f'----------------------------------------\n'
            f'Sugestão:\n{proposal}\n'
            f'----------------------------------------'
        )

        # Obtém a lista de e-mails dos administradores (que são as pessoas que receberão)
        recipient_list = [admin[1] for admin in settings.ADMINS]

        # 2. Envio do E-mail
        msg = EmailMessage(subject=subject, body=body, to=recipient_list, from_email=settings.DEFAULT_FROM_EMAIL)
        msg.send(fail_silently=False)  # fail_silently=False garante que erros levantem exceções

    except Exception as e:
        # 3. Tratamento de Erro e Logging
        error_message = (
            f"Falha ao enviar e-mail de sugestão. E-mail: {from_email}. Sugestão: '{proposal[:50]}...'. Erro: {e}"
        )
        # O logger 'proposal' gravará esta mensagem no rotating_file_handler
        logger.error(error_message, exc_info=True)


def send_proposal_email_async(from_email, proposal):
    """
    Função pública que inicia o envio do e-mail em uma thread separada.
    :param from_email: e-mail do usuário que sugeriu uma solução.
    :param proposal: Solução proposta pelo usuário.
    """
    # Cria e inicia a thread, passando a função privada e os argumentos
    t = threading.Thread(target=_send_email_in_thread, args=[from_email, proposal])
    t.start()

    # Retorna imediatamente para não bloquear a requisição do usuário
    return t
