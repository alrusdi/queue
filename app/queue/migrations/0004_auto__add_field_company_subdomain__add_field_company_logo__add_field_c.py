# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Company.subdomain'
        db.add_column('queue_company', 'subdomain', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True), keep_default=False)

        # Adding field 'Company.logo'
        db.add_column('queue_company', 'logo', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Company.info'
        db.add_column('queue_company', 'info', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Changing field 'MenuItemAttribute.field_description'
        db.alter_column('queue_menuitemattribute', 'field_description', self.gf('django.db.models.fields.TextField')(null=True))


    def backwards(self, orm):
        
        # Deleting field 'Company.subdomain'
        db.delete_column('queue_company', 'subdomain')

        # Deleting field 'Company.logo'
        db.delete_column('queue_company', 'logo')

        # Deleting field 'Company.info'
        db.delete_column('queue_company', 'info')

        # Changing field 'MenuItemAttribute.field_description'
        db.alter_column('queue_menuitemattribute', 'field_description', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))


    models = {
        'queue.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['queue.Company']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'queue.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['queue.MenuItem']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'queue.menuitemattribute': {
            'Meta': {'object_name': 'MenuItemAttribute'},
            'field_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'field_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.MenuItem']"})
        }
    }

    complete_apps = ['queue']
