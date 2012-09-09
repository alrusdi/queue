# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'MenuItemAttribute.field_value'
        db.delete_column('queue_menuitemattribute', 'field_value')

        # Adding field 'MenuItemAttribute.field_title'
        db.add_column('queue_menuitemattribute', 'field_title', self.gf('django.db.models.fields.CharField')(default='nope', max_length=255), keep_default=False)

        # Adding field 'MenuItemAttribute.field_description'
        db.add_column('queue_menuitemattribute', 'field_description', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'MenuItemAttribute.field_value'
        raise RuntimeError("Cannot reverse this migration. 'MenuItemAttribute.field_value' and its values cannot be restored.")

        # Deleting field 'MenuItemAttribute.field_title'
        db.delete_column('queue_menuitemattribute', 'field_title')

        # Deleting field 'MenuItemAttribute.field_description'
        db.delete_column('queue_menuitemattribute', 'field_description')


    models = {
        'queue.company': {
            'Meta': {'object_name': 'Company'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['queue.Company']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
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
            'field_description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'field_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.MenuItem']"})
        }
    }

    complete_apps = ['queue']
