"""
Daress Manager urls
"""

from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
		'',
		url(r'^$', 'manager.views.manager', name='index')
	)