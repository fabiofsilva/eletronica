from django.db import models
from django.urls import reverse as r
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .managers import ConsertoQuerySet


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
    diagnostico = models.TextField(verbose_name=_('Diagnostico e Sintomas'), null=True)
    slug = models.SlugField(verbose_name=_('Slug'), max_length=200, db_index=True, unique=True, editable=False)

    objects = ConsertoQuerySet.as_manager()

    class Meta:
        unique_together = ('modelo', 'defeito')
        ordering = ['id']

    def __str__(self):
        return f'{self.modelo.descricao} - {self.defeito.descricao}'

    def get_absolute_url(self):
        return r('core:conserto_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.modelo.descricao} - {self.defeito.descricao}')
        super().save(*args, **kwargs)


class Solucao(models.Model):
    conserto = models.ForeignKey('Conserto', verbose_name=_('Conserto'), on_delete=models.CASCADE)
    solucao = models.TextField(verbose_name=_('Solução'))

    class Meta:
        verbose_name = _('Solução')
        verbose_name_plural = _('Soluções')

    def __str__(self):
        return self.solucao[:30]
