# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Marca'
        db.create_table(u'core_marca', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'core', ['Marca'])

        # Adding unique constraint on 'Marca', fields ['descricao']
        db.create_unique(u'core_marca', ['descricao'])

        # Adding model 'Modelo'
        db.create_table(u'core_modelo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('marca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Marca'])),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'core', ['Modelo'])

        # Adding unique constraint on 'Modelo', fields ['marca', 'descricao']
        db.create_unique(u'core_modelo', ['marca_id', 'descricao'])

        # Adding model 'Defeito'
        db.create_table(u'core_defeito', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Defeito'])

        # Adding unique constraint on 'Defeito', fields ['descricao']
        db.create_unique(u'core_defeito', ['descricao'])

        # Adding model 'Conserto'
        db.create_table(u'core_conserto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modelo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Modelo'])),
            ('defeito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Defeito'])),
        ))
        db.send_create_signal(u'core', ['Conserto'])

        # Adding unique constraint on 'Conserto', fields ['modelo', 'defeito']
        db.create_unique(u'core_conserto', ['modelo_id', 'defeito_id'])

        # Adding model 'Solucao'
        db.create_table(u'core_solucao', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conserto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Conserto'])),
            ('solucao', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['Solucao'])


    def backwards(self, orm):
        # Removing unique constraint on 'Conserto', fields ['modelo', 'defeito']
        db.delete_unique(u'core_conserto', ['modelo_id', 'defeito_id'])

        # Removing unique constraint on 'Defeito', fields ['descricao']
        db.delete_unique(u'core_defeito', ['descricao'])

        # Removing unique constraint on 'Modelo', fields ['marca', 'descricao']
        db.delete_unique(u'core_modelo', ['marca_id', 'descricao'])

        # Removing unique constraint on 'Marca', fields ['descricao']
        db.delete_unique(u'core_marca', ['descricao'])

        # Deleting model 'Marca'
        db.delete_table(u'core_marca')

        # Deleting model 'Modelo'
        db.delete_table(u'core_modelo')

        # Deleting model 'Defeito'
        db.delete_table(u'core_defeito')

        # Deleting model 'Conserto'
        db.delete_table(u'core_conserto')

        # Deleting model 'Solucao'
        db.delete_table(u'core_solucao')


    models = {
        u'core.conserto': {
            'Meta': {'ordering': "('modelo__descricao', 'defeito__descricao')", 'unique_together': "(('modelo', 'defeito'),)", 'object_name': 'Conserto'},
            'defeito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Defeito']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modelo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Modelo']"})
        },
        u'core.defeito': {
            'Meta': {'ordering': "('descricao',)", 'unique_together': "(('descricao',),)", 'object_name': 'Defeito'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.marca': {
            'Meta': {'ordering': "('descricao',)", 'unique_together': "(('descricao',),)", 'object_name': 'Marca'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.modelo': {
            'Meta': {'ordering': "('marca__descricao', 'descricao')", 'unique_together': "(('marca', 'descricao'),)", 'object_name': 'Modelo'},
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Marca']"})
        },
        u'core.solucao': {
            'Meta': {'object_name': 'Solucao'},
            'conserto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Conserto']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solucao': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['core']