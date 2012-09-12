# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'VisitRequest'
        db.create_table('queue_visitrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.Company'])),
            ('visitor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.Visitor'])),
            ('visiting_point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.VisitingPoint'])),
        ))
        db.send_create_signal('queue', ['VisitRequest'])

        # Adding model 'VisitAttributes'
        db.create_table('queue_visitattributes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('visit_request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.VisitRequest'])),
            ('attr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.MenuItemAttribute'])),
            ('val', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('queue', ['VisitAttributes'])

        # Adding model 'Visitor'
        db.create_table('queue_visitor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('queue', ['Visitor'])

        # Adding model 'VisitingPoint'
        db.create_table('queue_visitingpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.MenuItem'])),
            ('operator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.Operator'])),
            ('date_from', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_to', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('queue', ['VisitingPoint'])

        # Adding model 'Operator'
        db.create_table('queue_operator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.Company'])),
        ))
        db.send_create_signal('queue', ['Operator'])


    def backwards(self, orm):
        
        # Deleting model 'VisitRequest'
        db.delete_table('queue_visitrequest')

        # Deleting model 'VisitAttributes'
        db.delete_table('queue_visitattributes')

        # Deleting model 'Visitor'
        db.delete_table('queue_visitor')

        # Deleting model 'VisitingPoint'
        db.delete_table('queue_visitingpoint')

        # Deleting model 'Operator'
        db.delete_table('queue_operator')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        },
        'queue.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.Company']"}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'field_type': ('django.db.models.fields.CharField', [], {'default': "'string'", 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.MenuItem']"})
        },
        'queue.operator': {
            'Meta': {'object_name': 'Operator'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'queue.visitattributes': {
            'Meta': {'object_name': 'VisitAttributes'},
            'attr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.MenuItemAttribute']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'val': ('django.db.models.fields.TextField', [], {}),
            'visit_request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.VisitRequest']"})
        },
        'queue.visitingpoint': {
            'Meta': {'object_name': 'VisitingPoint'},
            'date_from': ('django.db.models.fields.DateTimeField', [], {}),
            'date_to': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.Operator']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.MenuItem']"})
        },
        'queue.visitor': {
            'Meta': {'object_name': 'Visitor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'queue.visitrequest': {
            'Meta': {'object_name': 'VisitRequest'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.Company']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visiting_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.VisitingPoint']"}),
            'visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.Visitor']"})
        }
    }

    complete_apps = ['queue']
