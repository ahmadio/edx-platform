"""
Daress Manager urls
"""

from django.conf import settings
from djnaog.conf.urls import url, patterns, include

urlpatterns = patterns(
		'',
		url(r'^$', 'manager.views.manager', name='index')
	)