# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TestCenterUser'
        db.delete_table('student_testcenteruser')

        # Deleting model 'TestCenterRegistration'
        db.delete_table('student_testcenterregistration')


    def backwards(self, orm):
        # Adding model 'TestCenterUser'
        db.create_table('student_testcenteruser', (
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('suffix', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('confirmed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True, db_index=True)),
            ('salutation', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(blank=True, max_length=16, db_index=True)),
            ('processed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('phone_country_code', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('upload_status', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20, db_index=True)),
            ('upload_error_message', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50, db_index=True)),
            ('candidate_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('user_updated_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'], unique=True)),
            ('uploaded_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True, db_index=True)),
            ('extension', self.gf('django.db.models.fields.CharField')(blank=True, max_length=8, db_index=True)),
            ('fax_country_code', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=3, db_index=True)),
            ('client_candidate_id', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, db_index=True)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('address_3', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
        ))
        db.send_create_signal('student', ['TestCenterUser'])

        # Adding model 'TestCenterRegistration'
        db.create_table('student_testcenterregistration', (
            ('client_authorization_id', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True, db_index=True)),
            ('uploaded_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('user_updated_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('authorization_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_index=True)),
            ('upload_status', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20, db_index=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True, db_index=True)),
            ('confirmed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('accommodation_request', self.gf('django.db.models.fields.CharField')(max_length=1024, blank=True)),
            ('eligibility_appointment_date_first', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('exam_series_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('processed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('upload_error_message', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('accommodation_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('course_id', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('testcenter_user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['student.TestCenterUser'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eligibility_appointment_date_last', self.gf('django.db.models.fields.DateField')(db_index=True)),
        ))
        db.send_create_signal('student', ['TestCenterRegistration'])


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
        'student.courseenrollment': {
            'Meta': {'ordering': "('user', 'course_id')", 'unique_together': "(('user', 'course_id'),)", 'object_name': 'CourseEnrollment'},
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'default': "'honor'", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'student.courseenrollmentallowed': {
            'Meta': {'unique_together': "(('email', 'course_id'),)", 'object_name': 'CourseEnrollmentAllowed'},
            'auto_enroll': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'student.pendingemailchange': {
            'Meta': {'object_name': 'PendingEmailChange'},
            'activation_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_email': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'student.pendingnamechange': {
            'Meta': {'object_name': 'PendingNameChange'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rationale': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'student.registration': {
            'Meta': {'object_name': 'Registration', 'db_table': "'auth_registration'"},
            'activation_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'student.userprofile': {
            'Meta': {'object_name': 'UserProfile', 'db_table': "'auth_userprofile'"},
            'allow_certificate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'courseware': ('django.db.models.fields.CharField', [], {'default': "'course.xml'", 'max_length': '255', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'goals': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'level_of_education': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'mailing_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'year_of_birth': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'})
        },
        'student.userstanding': {
            'Meta': {'object_name': 'UserStanding'},
            'account_status': ('django.db.models.fields.CharField', [], {'max_length': '31', 'blank': 'True'}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standing_last_changed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'standing'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'student.usertestgroup': {
            'Meta': {'object_name': 'UserTestGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'db_index': 'True', 'symmetrical': 'False'})
        }
    }

    complete_apps = ['student']
