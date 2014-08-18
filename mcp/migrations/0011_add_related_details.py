# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Action.related_id'
        db.add_column(u'mcp_action', 'related_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Action.related_content'
        db.add_column(u'mcp_action', 'related_content',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Action.related_id'
        db.delete_column(u'mcp_action', 'related_id')

        # Deleting field 'Action.related_content'
        db.delete_column(u'mcp_action', 'related_content')


    models = {
        u'mcp.action': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Action'},
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'related_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'related_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'related_model': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['mcp.ActionStory']"}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1408351040'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['ttr.User']"})
        },
        u'mcp.actionstory': {
            'Meta': {'ordering': "['-last_timestamp']", 'object_name': 'ActionStory'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'first_timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1408351040'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1408351040', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'action_stories'", 'to': u"orm['ttr.User']"})
        },
        u'mcp.bulletin': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Bulletin'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bulletins'", 'to': u"orm['ttr.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'read_bulletins'", 'symmetrical': 'False', 'to': u"orm['ttr.User']"}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1408351040'}),
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
        u'mcp.shardcheckin': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'ShardCheckIn'},
            'channel': ('django.db.models.fields.IntegerField', [], {}),
            'cpu_usage': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'district_id': ('django.db.models.fields.IntegerField', [], {}),
            'fetched': ('django.db.models.fields.IntegerField', [], {'default': '1408351040'}),
            'frame_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '5'}),
            'heap_garbage': ('django.db.models.fields.IntegerField', [], {}),
            'heap_objects': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invasion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mem_usage': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
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
            'totp_secret': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['mcp']