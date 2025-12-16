from django.contrib import admin

from .models import Conserto, Defeito, Marca, Modelo, Solucao


class SolucaoInline(admin.StackedInline):
    model = Solucao
    extra = 1


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    search_fields = ['descricao']


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    search_fields = ['descricao', 'marca__descricao']
    autocomplete_fields = ['marca']


@admin.register(Defeito)
class DefeitoAdmin(admin.ModelAdmin):
    search_fields = ['descricao']


@admin.register(Conserto)
class ConsertoAdmin(admin.ModelAdmin):
    inlines = [SolucaoInline]
    ordering = ('modelo__descricao', 'defeito__descricao')
    search_fields = ['modelo__descricao', 'defeito__descricao']
    autocomplete_fields = ['defeito', 'modelo']
