# coding: utf-8
from django.views.generic import TemplateView
from django.urls import reverse_lazy as r
from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger
from eletronica.core.paginator import DiggPaginator as Paginator
from eletronica.core.models import Defeito, Conserto

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
        
def conserto_detail(request, pk):
    conserto = get_object_or_404(Conserto, pk=pk)
    return render(request, 'core/conserto_detail.html', {'conserto': conserto})