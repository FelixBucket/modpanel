# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Activity'
        db.delete_table(u'mcp_activity')

        # Adding model 'ActionStory'
        db.create_table(u'mcp_actionstory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_stories', to=orm['ttr.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('first_timestamp', self.gf('django.db.models.fields.IntegerField')(default=1408349206)),
            ('last_timestamp', self.gf('django.db.models.fields.IntegerField')(default=1408349206, db_index=True)),
        ))
        db.send_create_signal(u'mcp', ['ActionStory'])

        # Adding model 'Action'
        db.create_table(u'mcp_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['ttr.User'])),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('related_model', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')(default=1408349206)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['mcp.ActionStory'])),
            ('points', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mcp', ['Action'])


    def backwards(self, orm):
        # Adding model 'Activity'
        db.create_table(u'mcp_activity', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')(default=1408212509)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activity', null=True, to=orm['ttr.User'], blank=True)),
            ('action', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'mcp', ['Activity'])

        # Deleting model 'ActionStory'
        db.delete_table(u'mcp_actionstory')

        # Deleting model 'Action'
        db.delete_table(u'mcp_action')


    models = {
        u'mcp.action': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Action'},
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'related_model': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['mcp.ActionStory']"}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1408349206'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['ttr.User']"})
        },
        u'mcp.actionstory': {
            'Meta': {'ordering': "['-last_timestamp']", 'object_name': 'ActionStory'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'first_timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1408349206'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1408349206', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'action_stories'", 'to': u"orm['ttr.User']"})
        },
        u'mcp.bulletin': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Bulletin'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bulletins'", 'to': u"orm['ttr.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'read_bulletins'", 'symmetrical': 'False', 'to': u"orm['ttr.User']"}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'default': '1408349206'}),
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
            'fetched': ('django.db.models.fields.IntegerField', [], {'default': '1408349206'}),
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