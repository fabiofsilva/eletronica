from django.contrib import admin

from .models import Conserto, Defeito, Marca, Modelo, Solucao


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
