from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from .forms import SugestaoSolucaoForm
from .models import Conserto, Defeito
from .paginator import DiggPaginator as Paginator
from .tasks import send_proposal_email_async


class HomePageView(TemplateView):
    template_name = 'core/homepage.html'


def search_repair(request):
    return render(request, 'core/search_repair.html', {'defeitos': Defeito.objects.all()})


def conserto_list(request):
    filters = {}
    add_filter(request, filters, 'marca', 'modelo__marca__descricao')
    add_filter(request, filters, 'modelo', 'modelo__descricao')
    add_filter(request, filters, 'defeito', field_lookup='')
    queryset = Conserto.objects.filter(**filters)
    paginator = Paginator(queryset, 20, body=5)
    page = request.POST.get('page', 1)
    try:
        consertos = paginator.page(page)
    except PageNotAnInteger:
        consertos = paginator.page(1)
    except EmptyPage:
        consertos = paginator.page(paginator.num_pages)
    return render(request, 'core/conserto_list.html', {'consertos': consertos})


def add_filter(request, dictionary, field, field_name='', field_lookup='__icontains'):
    if request.method == 'GET':
        rmethod = request.GET
    else:
        rmethod = request.POST

    value = rmethod.get(field)
    if value:
        fname = field_name if field_name else field
        dictionary.update({fname + field_lookup: value})


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
