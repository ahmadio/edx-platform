"""
URL mappings for the daress_manager
"""

from django.conf.urls import patterns, url


urlpatterns = patterns('daress_manager.views',  # nopep8
                       url(r'^$', 'index', name='daress_manager_index'),
)
