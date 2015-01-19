"""
View endpoints for daress_manager
"""
from datetime import datetime
import pytz
from django.conf import settings
from django.contrib.auth.models import Group
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
    HttpResponseBadRequest, HttpResponseForbidden, Http404
)
from util.json_request import JsonResponse, expect_json
from django.views.decorators.http import require_POST, require_http_methods
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from edxmako.shortcuts import render_to_response
from shoppingcart.models import Order, OrderItem

from direct_payments.models import Charge, UserBalance

@login_required
def index(request):
    """
    This view shows daress manager index
    """
    if not request.user.is_superuser:
        return HttpResponseBadRequest()

    all_charges = Charge.objects.exclude(status='approved')
    print all_charges
    context = {
        'all_charges': all_charges
    }
    return render_to_response("daress_manager/index.html", context)
