# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Activity'
        db.create_table(u'mcp_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='activity', null=True, to=orm['ttr.User'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')(default=1408069707)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'mcp', ['Activity'])


    def backwards(self, orm):
        # Deleting model 'Activity'
        db.delete_table(u'mcp_activity')


    models = {
        u'mcp.activity': {
            'Meta': {'object_name': 'Activity'},
            'action': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1408069707'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'activity'", 'null': 'True', 'to': u"orm['ttr.User']"})
        },
        u'mcp.bulletin': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Bulletin'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bulletins'", 'to': u"orm['ttr.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'read_bulletins'", 'symmetrical': 'False', 'to': u"orm['ttr.User']"}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1408069707'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mcp.modprofile': {
            'Meta': {'object_name': 'ModProfile'},
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'mod_profile'", 'unique': 'True', 'to': u"orm['ttr.User']"})
        },
        u'ttr.user': {
            'Meta': {'object_name': 'User', 'db_table': "'user'", 'managed': 'False'},
            'activate_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'gs_user_id': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'type'", 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'register_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'register_ip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'toonbook_user_id': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True'}),
            'totp_secret': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['mcp']