# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PPPUmfrage'
        db.create_table('ppp_pppumfrage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ppp_start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('ppp_end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('ppp', ['PPPUmfrage'])

        # Adding model 'Student'
        db.create_table('ppp_student', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('umfrage', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matrikelnummern', null=True, to=orm['ppp.PPPUmfrage'])),
            ('matrikelnummer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('geburtstag', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('ppp', ['Student'])

        # Adding model 'Nominierung'
        db.create_table('ppp_nominierung', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('umfrage', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nominierungen', null=True, to=orm['ppp.PPPUmfrage'])),
            ('typ', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('person', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('ppp', ['Nominierung'])


    def backwards(self, orm):
        
        # Deleting model 'PPPUmfrage'
        db.delete_table('ppp_pppumfrage')

        # Deleting model 'Student'
        db.delete_table('ppp_student')

        # Deleting model 'Nominierung'
        db.delete_table('ppp_nominierung')


    models = {
        'ppp.nominierung': {
            'Meta': {'object_name': 'Nominierung'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'typ': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'umfrage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nominierungen'", 'null': 'True', 'to': "orm['ppp.PPPUmfrage']"})
        },
        'ppp.pppumfrage': {
            'Meta': {'object_name': 'PPPUmfrage'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ppp_end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'ppp_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'ppp.student': {
            'Meta': {'object_name': 'Student'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'geburtstag': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matrikelnummer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'umfrage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matrikelnummern'", 'null': 'True', 'to': "orm['ppp.PPPUmfrage']"})
        }
    }

    complete_apps = ['ppp']
