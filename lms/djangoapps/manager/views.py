from django.http import HttpResponse
from edxmako.shortcuts import render_to_response


def manager(request):

	return render_to_response('manager/pages-admin-theme-main.html', {})