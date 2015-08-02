from django.http import HttpResponse


def manager(request):
	return HttpResponse('"<html><body>helelleleo.</body></html>"')