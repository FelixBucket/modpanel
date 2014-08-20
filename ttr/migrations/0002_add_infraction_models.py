# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InfractionSubject'
        db.create_table('infractions_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=39)),
            ('infraction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ttr.Infraction'])),
            ('barbed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'ttr', ['InfractionSubject'])

        # Adding model 'Infraction'
        db.create_table('infractions_infraction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('external_reason', self.gf('django.db.models.fields.TextField')()),
            ('internal_reason', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('moderator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ttr.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('approved', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('decided', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expiration', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('change_level', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('speedchat_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_true_friends', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_community_areas', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'ttr', ['Infraction'])


    def backwards(self, orm):
        # Deleting model 'InfractionSubject'
        db.delete_table('infractions_subject')

        # Deleting model 'Infraction'
        db.delete_table('infractions_infraction')


    models = {
        u'ttr.infraction': {
            'Meta': {'object_name': 'Infraction', 'db_table': "'infractions_infraction'"},
            'approved': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'change_level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'decided': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'expiration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'external_reason': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_reason': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ttr.User']"}),
            'no_community_areas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_true_friends': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'speedchat_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'ttr.infractionsubject': {
            'Meta': {'object_name': 'InfractionSubject', 'db_table': "'infractions_subject'"},
            'barbed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'identifier_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'infraction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ttr.Infraction']"})
        },
        u'ttr.newsitem': {
            'Meta': {'object_name': 'NewsItem', 'db_table': "'news_item'", 'managed': 'False'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ttr.User']", 'null': 'True'}),
            'author_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'release_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'ttr.newsitemcomment': {
            'Meta': {'ordering': "['id']", 'object_name': 'NewsItemComment', 'db_table': "'comment'", 'managed': 'False'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'css': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'db_column': "'ip'"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ttr.NewsItemComment']", 'null': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ttr.NewsItem']", 'null': 'True'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ttr.User']", 'null': 'True'})
        },
        u'ttr.scheduledsession': {
            'Meta': {'object_name': 'ScheduledSession', 'db_table': "'scheduled_session'", 'managed': 'False'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ttr.User']", 'null': 'True'})
        },
        u'ttr.toonname': {
            'Meta': {'ordering': "['received']", 'object_name': 'ToonName', 'db_table': "'toon_name'", 'managed': 'False'},
            'candidate_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'current_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'received': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ttr.User']", 'null': 'True', 'blank': 'True'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'toon_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'was_rejected': ('django.db.models.fields.BooleanField', [], {})
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

    complete_apps = ['ttr']