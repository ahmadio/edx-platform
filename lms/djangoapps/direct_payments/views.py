"""
View endpoints for direct payments
"""

from django.conf import settings
from django.contrib.auth.models import Group
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
    HttpResponseBadRequest, HttpResponseForbidden, Http404
)
from util.json_request import JsonResponse, expect_json
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from edxmako.shortcuts import render_to_response

from .models import Charge

@login_required
def index(request):
    """
    This view shows direct_payments_form
    """
    charges = Charge.objects.filter(user=request.user)
    context = {
        'charges':charges
    }
    return render_to_response("direct_payments/index.html", context)


@login_required
def new_charge(request):
    """
    create new charge with amount and attachment image and user notes
    """
    if request.method == 'POST':
        attachment = request.FILES.get('attachment', None)
        if attachment:
            c = Charge(user=request.user,
                   amount=request.POST.get('amount', 0),
                   user_notes=request.POST.get('user_notes', "NoNo"),
                   attachment=request.FILES['attachment'])
            c.save()
            return redirect('dashboard')
        
        return JsonResponse({'msg':'No files attached'}, status=400)
    
    return JsonResponse({'msg':'Bad Request'}, status=400)
  
    
@login_required
def remove_charge_entry(request):
    """
    this will mark the charge entry as "is_shown=False" and won't actually remove it
    """
    if request.method == 'POST':
        charge_id = int(request.POST['charge']) if request.POST.get('charge', None) else None
        if charge_id:
            try:
                c = Charge.objects.get(pk=charge_id)
                if c.user == request.user or request.user.is_superuser:
                    c.hide()
                    return JsonResponse({'msg':'Removed'}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'msg':'Charge not found'}, status=404)
        else:
            return JsonResponse({'msg':'Missig paramaters'}, status=400)
    
    return JsonResponse({'msg':'Bad Request'}, status=400)


@login_required
def update_charge_amount(request):
    """
    update the initial charge amount
    """
    if request.method == 'POST':
        charge_id = int(request.POST['charge']) if request.POST.get('charge', None) else None
        new_amount = int(request.POST['new_amount']) if request.POST.get('new_amount', None) else None
        if charge_id & new_amount:
            try:
                c = Charge.objects.get(pk=charge_id)
                if c.user == request.user or request.user.is_superuser:
                    c.amount = new_amount
                    c.save()
                    return JsonResponse({'msg':'Updated'}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'msg':'Charge not found'}, status=404)
        else:
            return JsonResponse({'msg':'Missig paramaters'}, status=400)
        
    return JsonResponse({'msg':'Bad Request'}, status=400)


@login_required
def update_charge_status(request):
    """
    update charge status
    """
    if request.method == 'POST':
        charge_id = int(request.POST['charge']) if request.POST.get('charge', None) else None
        status = request.POST.get('status', None)
        if charge_id and status:
            try:
                c = Charge.objects.get(pk=charge_id)
                if status not in ['pending', 'rejected', 'canceled', 'approved']:
                    return JsonResponse({'msg':'Not supported'}, status=400)
                if c.user == request.user or request.user.is_superuser:
                    c.update_status(status, request)
                    return JsonResponse({'msg':'Updated'}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'msg':'Charge not found'}, status=404)
        else:
            return JsonResponse({'msg':'Missig paramaters'}, status=400)
        
    return JsonResponse({'msg':'Bad Request'}, status=400)


@login_required
def add_charge_comment(request):
    """
    add comment to charge entry
    """
    if request.method == 'POST':
        charge_id = int(request.POST['charge']) if request.POST.get('charge', None) else None
        content = request.POST.get('content', None)
        if charge_id and content:
            try:
                c = Charge.objects.get(pk=charge_id)
                if len(content) < 1:
                    return JsonResponse({'msg':'provide comment'}, status=400)
                if c.user == request.user or request.user.is_superuser:
                    c.add_comment(content, request)
                    return JsonResponse({'msg':'Comment added'}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'msg':'Charge not found'}, status=404)
        else:
            return JsonResponse({'msg':'Missig paramaters'}, status=400)
        
    return JsonResponse({'msg':'Bad Request'}, status=400)
    