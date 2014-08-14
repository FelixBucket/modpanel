# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ModProfile.user'
        db.alter_column(u'mcp_modprofile', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['ttr.User']))
        # Adding unique constraint on 'ModProfile', fields ['user']
        db.create_unique(u'mcp_modprofile', ['user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ModProfile', fields ['user']
        db.delete_unique(u'mcp_modprofile', ['user_id'])


        # Changing field 'ModProfile.user'
        db.alter_column(u'mcp_modprofile', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ttr.User']))

    models = {
        u'mcp.bulletin': {
            'Meta': {'object_name': 'Bulletin'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bulletins'", 'to': u"orm['ttr.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'read_bulletins'", 'symmetrical': 'False', 'to': u"orm['ttr.User']"}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1408044745'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mcp.modprofile': {
            'Meta': {'object_name': 'ModProfile'},
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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