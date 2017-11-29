# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse as r


class Marca(models.Model):
    descricao = models.CharField(verbose_name=_(u'Marca'), max_length=50)
    
    class Meta:
        unique_together = ('descricao',)
        ordering = ('descricao',)
         
    def __unicode__(self):
        return self.descricao
    
class Modelo(models.Model):
    marca = models.ForeignKey('Marca', verbose_name=_(u'Marca'), on_delete=models.PROTECT)
    descricao = models.CharField(verbose_name=_(u'Modelo'), max_length=50)
    
    class Meta:
        unique_together = ('marca', 'descricao')
        ordering = ('marca__descricao', 'descricao')
    
    def __unicode__(self):
        return self.marca.descricao + u' - ' + self.descricao 

class Defeito(models.Model):
    descricao = models.CharField(verbose_name=_(u'Defeito'), max_length=100)
    
    class Meta:
        unique_together = ('descricao',)
        ordering = ('descricao',)
        
    def __unicode__(self):
        return self.descricao
    
class Conserto(models.Model):
    modelo = models.ForeignKey('Modelo', verbose_name=_(u'Modelo'), on_delete=models.PROTECT)
    defeito = models.ForeignKey('Defeito', verbose_name=_(u'Defeito'), on_delete=models.PROTECT)
    
    class Meta:
        unique_together = ('modelo', 'defeito')
        ordering = ['id']
        
    def __unicode__(self):
        return self.modelo.descricao + u' - ' + self.defeito.descricao
    
    def get_absolute_url(self):
        return r('core:conserto_detail', kwargs={'pk': self.pk})
    
class Solucao(models.Model):
    conserto = models.ForeignKey('Conserto', verbose_name=_(u'Conserto'), on_delete=models.CASCADE)
    solucao = models.TextField(verbose_name=_(u'Solução'))
    
    class Meta:
        verbose_name = _(u'Solução')
        verbose_name_plural = _(u'Soluções')
        
    def __unicode__(self):
        return self.solucao[:30]