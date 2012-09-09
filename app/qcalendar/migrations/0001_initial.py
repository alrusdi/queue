# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Calendar'
        db.create_table('qcalendar_calendar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.Company'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('qcalendar', ['Calendar'])

        # Adding model 'Day'
        db.create_table('qcalendar_day', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['qcalendar.Calendar'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('is_short', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_weekend', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_holiday', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('qcalendar', ['Day'])


    def backwards(self, orm):
        
        # Deleting model 'Calendar'
        db.delete_table('qcalendar_calendar')

        # Deleting model 'Day'
        db.delete_table('qcalendar_day')


    models = {
        'qcalendar.calendar': {
            'Meta': {'object_name': 'Calendar'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.Company']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'qcalendar.day': {
            'Meta': {'object_name': 'Day'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['qcalendar.Calendar']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_holiday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_short': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_weekend': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
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
        }
    }

    complete_apps = ['qcalendar']
