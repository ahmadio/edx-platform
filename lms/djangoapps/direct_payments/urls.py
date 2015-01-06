"""
URL mappings for the direct payments
"""

from django.conf.urls import patterns, url


urlpatterns = patterns('direct_payments.views',  # nopep8
                       url(r'^$', 'index', name='direct_payments_index'),
                       url(r'^new_charge$', 'new_charge', name='new_charge'),
                       url(r'^remove_charge_entry$', 'remove_charge_entry', name='remove_charge_entry'),
                       url(r'^update_charge_amount$', 'update_charge_amount', name='update_charge_amount'),
                       url(r'^update_charge_status$', 'update_charge_status', name='update_charge_status'),
                       url(r'^add_charge_comment$', 'add_charge_comment', name='add_charge_comment'),
                       url(r'^direct_purchase_order$', 'direct_purchase_order', name='direct_purchase_order'),

)
