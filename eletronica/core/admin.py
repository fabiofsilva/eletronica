# coding: utf-8
from django.contrib import admin
from eletronica.core.models import Marca, Modelo, Defeito, Solucao, Conserto


class SolucaoInline(admin.StackedInline):
    model = Solucao
    extra = 1

class ConsertoAdmin(admin.ModelAdmin):
    model = Conserto
    inlines = [SolucaoInline]
    ordering = ('modelo__descricao', 'defeito__descricao')
    
admin.site.register(Marca, admin.ModelAdmin)
admin.site.register(Modelo, admin.ModelAdmin)
admin.site.register(Defeito, admin.ModelAdmin)
admin.site.register(Conserto, ConsertoAdmin)