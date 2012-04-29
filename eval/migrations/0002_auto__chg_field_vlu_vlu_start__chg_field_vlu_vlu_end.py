# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Vlu.vlu_start'
        db.alter_column('eval_vlu', 'vlu_start', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Vlu.vlu_end'
        db.alter_column('eval_vlu', 'vlu_end', self.gf('django.db.models.fields.DateTimeField')())


    def backwards(self, orm):
        
        # Changing field 'Vlu.vlu_start'
        db.alter_column('eval_vlu', 'vlu_start', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Vlu.vlu_end'
        db.alter_column('eval_vlu', 'vlu_end', self.gf('django.db.models.fields.DateField')())


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 24, 11, 24, 1, 849711)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 24, 11, 24, 1, 849627)'}),
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
        'eval.antwort': {
            'Meta': {'object_name': 'Antwort'},
            'antwortbogen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'antworten'", 'to': "orm['eval.Antwortbogen']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'frage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eval.Frage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eval.Option']", 'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'eval.antwortbogen': {
            'Meta': {'object_name': 'Antwortbogen'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'studiengang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eval.Studiengang']", 'null': 'True', 'blank': 'True'}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'antwortboegen_tutor'", 'null': 'True', 'to': "orm['eval.Personal']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'boegen'", 'null': 'True', 'to': "orm['auth.User']"}),
            'vorlesung': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'antwortboegen'", 'to': "orm['eval.Vorlesung']"})
        },
        'eval.frage': {
            'Meta': {'object_name': 'Frage'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fragentyp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eval.Fragentyp']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'eval.fragebogen': {
            'Meta': {'object_name': 'Fragebogen'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fragensets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'frageboegen'", 'symmetrical': 'False', 'through': "orm['eval.FragensetFragebogen']", 'to': "orm['eval.Fragenset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'eval.fragefragenset': {
            'Meta': {'ordering': "['rank']", 'object_name': 'FrageFragenset'},
            'frage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eval.Frage']"}),
            'fragenset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eval.Fragenset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'eval.fragenset': {
            'Meta': {'object_name': 'Fragenset'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fragen': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'fragensets'", 'symmetrical': 'False', 'through': "orm['eval.FrageFragenset']", 'to': "orm['eval.Frage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'titel': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'eval.fragensetfragebogen': {
            'Meta': {'ordering': "['rank']", 'object_name': 'FragensetFragebogen'},
            'fragebogen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eval.Fragebogen']"}),
            'fragenset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eval.Fragenset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'eval.fragentyp': {
            'Meta': {'object_name': 'Fragentyp'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'texttype': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'eval.option': {
            'Meta': {'ordering': "['rank']", 'object_name': 'Option'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fragentyp': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'optionen'", 'to': "orm['eval.Fragentyp']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'eval.personal': {
            'Meta': {'object_name': 'Personal'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'personaltyp': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eval.Personaltyp']", 'null': 'True', 'blank': 'True'}),
            'titel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'eval.personaltyp': {
            'Meta': {'object_name': 'Personaltyp'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'eval.studiengang': {
            'Meta': {'object_name': 'Studiengang'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'eval.vlu': {
            'Meta': {'object_name': 'Vlu'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'vlu_end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'vlu_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'eval.vorlesung': {
            'Meta': {'object_name': 'Vorlesung'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'dozenten': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'vorlesungen'", 'symmetrical': 'False', 'to': "orm['eval.Personal']"}),
            'fragebogen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vorlesungen'", 'to': "orm['eval.Fragebogen']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tutoren': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'vorlesungen_tutor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['eval.Personal']"}),
            'vlu': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vorlesungen'", 'to': "orm['eval.Vlu']"})
        }
    }

    complete_apps = ['eval']
