import logging
import datetime
import decimal
import pytz
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.core.context_processors import csrf
from django.http import (HttpResponse, HttpResponseBadRequest, HttpResponseForbidden,
                         HttpResponseServerError, Http404)
from django.shortcuts import redirect

log = logging.getLogger("shoppingcart")
AUDIT_LOG = logging.getLogger("audit")

@require_POST
@login_required
@ensure_csrf_cookie
def create_paypal_payment(request):
	print request.POST 
	return HttpResponse()