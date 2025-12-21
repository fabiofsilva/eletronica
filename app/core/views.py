from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from .forms import SugestaoSolucaoForm
from .models import Conserto, Defeito
from .tasks import send_proposal_email_async


class HomePageView(TemplateView):
    template_name = 'core/homepage.html'


def search_repair(request):
    return render(request, 'core/search_repair.html', {'defeitos': Defeito.objects.all()})


def conserto_detail(request, slug):
    conserto = get_object_or_404(Conserto.objects.select_related('modelo', 'defeito'), slug=slug)

    if conserto.diagnostico:
        seo_description = conserto.diagnostico
    else:
        seo_description = (
            f'Diagnóstico do defeito {conserto.defeito.descricao} '
            f'no modelo {conserto.modelo.descricao}. '
            'Veja sintomas comuns, possíveis causas e soluções.'
        )

    context = {
        'conserto': conserto,
        'seo_title': f'{conserto.modelo.descricao} - {conserto.defeito}',
        'seo_description': seo_description,
    }
    return render(request, 'core/conserto_detail.html', context)


def sugestao_solucao(request):
    if request.method == 'GET':
        form = SugestaoSolucaoForm()
    else:
        form = SugestaoSolucaoForm(request.POST)

        if form.is_valid():
            send_proposal_email_async(form.cleaned_data['email'], form.cleaned_data['sugestao'])
            messages.success(request, 'Obrigado! Os administradores foram notificados sobre a sua sugestão.')
            return redirect('core:homepage')

    return render(request, 'core/sugestao_solucao.html', context={'form': form, 'noindex': True})
