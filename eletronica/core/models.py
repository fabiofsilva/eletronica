from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse as r


class Marca(models.Model):
    descricao = models.CharField(verbose_name=_('Marca'), max_length=50)

    class Meta:
        unique_together = ('descricao',)
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao


class Modelo(models.Model):
    marca = models.ForeignKey('Marca', verbose_name=_('Marca'), on_delete=models.PROTECT)
    descricao = models.CharField(verbose_name=_('Modelo'), max_length=50)

    class Meta:
        unique_together = ('marca', 'descricao')
        ordering = ('marca__descricao', 'descricao')

    def __str__(self):
        return f'{self.marca.descricao} - {self.descricao}'


class Defeito(models.Model):
    descricao = models.CharField(verbose_name=_('Defeito'), max_length=100)

    class Meta:
        unique_together = ('descricao',)
        ordering = ('descricao',)

    def __str__(self):
        return self.descricao


class Conserto(models.Model):
    modelo = models.ForeignKey('Modelo', verbose_name=_('Modelo'), on_delete=models.PROTECT)
    defeito = models.ForeignKey('Defeito', verbose_name=_('Defeito'), on_delete=models.PROTECT)

    class Meta:
        unique_together = ('modelo', 'defeito')
        ordering = ['id']

    def __str__(self):
        return f'{self.modelo.descricao} - {self.defeito.descricao}'

    def get_absolute_url(self):
        return r('core:conserto_detail', kwargs={'pk': self.pk})


class Solucao(models.Model):
    conserto = models.ForeignKey('Conserto', verbose_name=_('Conserto'), on_delete=models.CASCADE)
    solucao = models.TextField(verbose_name=_('Solução'))

    class Meta:
        verbose_name = _('Solução')
        verbose_name_plural = _('Soluções')

    def __str__(self):
        return self.solucao[:30]
