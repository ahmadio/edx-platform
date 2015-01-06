# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Charge'
        db.create_table('direct_payments_charge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='charges', to=orm['auth.User'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=30, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(default='usd', max_length=8)),
            ('attachment', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('user_notes', self.gf('django.db.models.fields.TextField')(default="User didn't provide notes")),
            ('reviewer_notes', self.gf('django.db.models.fields.TextField')(default="Reviewer didn't provide notes")),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=32)),
            ('is_shown', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('direct_payments', ['Charge'])

        # Adding model 'Deposit'
        db.create_table('direct_payments_deposit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='deposits', to=orm['auth.User'])),
            ('charge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['direct_payments.Charge'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='approved_deposits', to=orm['auth.User'])),
        ))
        db.send_create_signal('direct_payments', ['Deposit'])

        # Adding unique constraint on 'Deposit', fields ['user', 'charge']
        db.create_unique('direct_payments_deposit', ['user_id', 'charge_id'])

        # Adding model 'Comment'
        db.create_table('direct_payments_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='charge_comments', to=orm['auth.User'])),
            ('charge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['direct_payments.Charge'])),
            ('content', self.gf('django.db.models.fields.TextField')(default='empty comment')),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('direct_payments', ['Comment'])

        # Adding model 'UserBalance'
        db.create_table('direct_payments_userbalance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='balance', unique=True, to=orm['auth.User'])),
            ('current_balance', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=30, decimal_places=2)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('history', self.gf('django.db.models.fields.TextField')(default='{}')),
        ))
        db.send_create_signal('direct_payments', ['UserBalance'])

        # Adding model 'OnHoldPaidRegistration'
        db.create_table('direct_payments_onholdpaidregistration', (
            ('orderitem_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['shoppingcart.OrderItem'], unique=True, primary_key=True)),
            ('course_id', self.gf('xmodule_django.models.CourseKeyField')(max_length=128, db_index=True)),
            ('mode', self.gf('django.db.models.fields.SlugField')(default='honor', max_length=50)),
        ))
        db.send_create_signal('direct_payments', ['OnHoldPaidRegistration'])


    def backwards(self, orm):
        # Removing unique constraint on 'Deposit', fields ['user', 'charge']
        db.delete_unique('direct_payments_deposit', ['user_id', 'charge_id'])

        # Deleting model 'Charge'
        db.delete_table('direct_payments_charge')

        # Deleting model 'Deposit'
        db.delete_table('direct_payments_deposit')

        # Deleting model 'Comment'
        db.delete_table('direct_payments_comment')

        # Deleting model 'UserBalance'
        db.delete_table('direct_payments_userbalance')

        # Deleting model 'OnHoldPaidRegistration'
        db.delete_table('direct_payments_onholdpaidregistration')


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
        'direct_payments.charge': {
            'Meta': {'object_name': 'Charge'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '30', 'decimal_places': '2'}),
            'attachment': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'usd'", 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shown': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'reviewer_notes': ('django.db.models.fields.TextField', [], {'default': '"Reviewer didn\'t provide notes"'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'charges'", 'to': "orm['auth.User']"}),
            'user_notes': ('django.db.models.fields.TextField', [], {'default': '"User didn\'t provide notes"'})
        },
        'direct_payments.comment': {
            'Meta': {'object_name': 'Comment'},
            'charge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['direct_payments.Charge']"}),
            'content': ('django.db.models.fields.TextField', [], {'default': "'empty comment'"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'charge_comments'", 'to': "orm['auth.User']"})
        },
        'direct_payments.deposit': {
            'Meta': {'unique_together': "(('user', 'charge'),)", 'object_name': 'Deposit'},
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'approved_deposits'", 'to': "orm['auth.User']"}),
            'charge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['direct_payments.Charge']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deposits'", 'to': "orm['auth.User']"})
        },
        'direct_payments.onholdpaidregistration': {
            'Meta': {'object_name': 'OnHoldPaidRegistration', '_ormbases': ['shoppingcart.OrderItem']},
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'max_length': '128', 'db_index': 'True'}),
            'mode': ('django.db.models.fields.SlugField', [], {'default': "'honor'", 'max_length': '50'}),
            'orderitem_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['shoppingcart.OrderItem']", 'unique': 'True', 'primary_key': 'True'})
        },
        'direct_payments.userbalance': {
            'Meta': {'object_name': 'UserBalance'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '30', 'decimal_places': '2'}),
            'history': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'balance'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'shoppingcart.order': {
            'Meta': {'object_name': 'Order'},
            'bill_to_cardtype': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'bill_to_ccnum': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'bill_to_city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'bill_to_country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'bill_to_first': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'bill_to_last': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'bill_to_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'bill_to_state': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'bill_to_street1': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'bill_to_street2': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'company_contact_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'company_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'usd'", 'max_length': '8'}),
            'customer_reference_number': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_type': ('django.db.models.fields.CharField', [], {'default': "'personal'", 'max_length': '32'}),
            'processor_reply_dump': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'purchase_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipient_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'recipient_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'refunded_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'cart'", 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'shoppingcart.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'usd'", 'max_length': '8'}),
            'fulfilled_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_desc': ('django.db.models.fields.CharField', [], {'default': "'Misc. Item'", 'max_length': '1024'}),
            'list_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '30', 'decimal_places': '2'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shoppingcart.Order']"}),
            'qty': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'refund_requested_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'report_comments': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'service_fee': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '30', 'decimal_places': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'cart'", 'max_length': '32', 'db_index': 'True'}),
            'unit_cost': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '30', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['direct_payments']