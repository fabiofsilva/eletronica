from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _


def seo_defaults(request):
    """
    Context processor responsável por fornecer valores padrão de SEO
    para todas as páginas da aplicação.

    Objetivos:
    - Garantir que SEMPRE existam variáveis básicas de SEO no contexto
    - Evitar páginas sem <title>, meta description ou Open Graph image
    - Centralizar defaults para facilitar manutenção e testes

    As views podem sobrescrever qualquer uma dessas variáveis quando
    precisarem de SEO específico.
    """

    return {
        'seo_title': _('Plataforma de Diagnóstico'),
        'seo_description': _('Encontre diagnósticos, defeitos e soluções técnicas para diversos modelos.'),
        'noindex': False,
        'seo_image': request.build_absolute_uri(static('img/og-diagnostico-eletronicos.jpg')),
    }
